from typing import Iterable

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from newsflash import FunctionRegistry
from newsflash.models import Element
from newsflash.elements import Notification

from ping_pong_pals.database import get_db
from ping_pong_pals.database.crud import (
    get_all_users,
    save_game,
    get_id_for_username,
)

from .elements import (
    WinnerSelect,
    WinnerPointsInput,
    LoserSelect,
    LoserPointsInput,
    SubmitGameButton,
)


function_registry = FunctionRegistry()


@function_registry.add(on=WinnerSelect().search())
def winner_select_search(winner_select: WinnerSelect) -> Iterable[Element]:
    db = get_db()
    try:
        _, all_usernames = get_all_users(db=db)
    finally:
        db.close()

    yield winner_select.with_options(options=all_usernames)


@function_registry.add(on=WinnerSelect().select())
def winner_selected(winner_select: WinnerSelect) -> Iterable[Element]:
    yield winner_select


@function_registry.add(on=LoserSelect().search())
def loser_select_search(loser_select: LoserSelect) -> Iterable[Element]:
    db = get_db()
    try:
        _, all_usernames = get_all_users(db=db)
    finally:
        db.close()

    yield loser_select.with_options(options=all_usernames)


@function_registry.add(on=LoserSelect().select())
def loser_selected(loser_select: LoserSelect) -> Iterable[Element]:
    yield loser_select


@function_registry.add(on=SubmitGameButton().click())
def register_new_game(
    winner_select: WinnerSelect,
    winner_points_input: WinnerPointsInput,
    loser_select: LoserSelect,
    loser_points_input: LoserPointsInput,
) -> Iterable[Element]:
    if winner_select.value == "" or loser_select.value == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="please fill in the required fields",
        )

    db = get_db()
    try:
        winner_user_id = get_id_for_username(db=db, username=winner_select.value)
        loser_user_id = get_id_for_username(db=db, username=loser_select.value)

        if winner_user_id is None or loser_user_id is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="something went wrong",
            )
        
        save_game(
            db=db,
            winner=winner_user_id,
            loser=loser_user_id,
            winner_points=winner_points_input.value,
            loser_points=loser_points_input.value,
        )

        yield WinnerSelect()
        yield WinnerPointsInput()
        yield LoserSelect()
        yield LoserPointsInput()

        yield Notification(message="Game successfully stored!")
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="something went wrong",
        )
    finally:
        db.close()
