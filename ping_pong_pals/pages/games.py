from collections.abc import Iterable

from fastapi import HTTPException, status
from newsflash import FunctionRegistry, Page
from newsflash.elements import (
    Button,
    Header,
    InputInteger,
    Notification,
    NotificationContainer,
    Paragraph,
    Select,
    Vertical,
)
from newsflash.models import Element
from sqlalchemy.exc import IntegrityError

from ping_pong_pals.database import get_db
from ping_pong_pals.database.crud import (
    get_all_usernames,
    get_user_from_session,
    save_game,
)
from ping_pong_pals.elements import NavigationLinks

function_registry = FunctionRegistry()


class WinnerSelect(Select):
    id: str = "winner-select"


class WinnerPointsInput(InputInteger):
    id: str = "winner-points-input"
    placeholder: str = "winner points"
    value: int = 11


class LoserSelect(Select):
    id: str = "loser-select"


class LoserPointsInput(InputInteger):
    id: str = "loser-points-input"
    placeholder: str = "loser points"


class SubmitGameButton(Button):
    id: str = "submit-game-button"
    label: str = "Submit Game"


@function_registry.add(on=WinnerSelect().search())
def winner_select_search(winner_select: WinnerSelect) -> Iterable[Element]:
    db = get_db()
    try:
        all_usernames = get_all_usernames(db=db)
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
        all_usernames = get_all_usernames(db=db)
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
        save_game(
            db=db,
            winner=winner_select.value,
            loser=loser_select.value,
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


class GamesPage(Page):
    path: str = "/games"
    page_title: str = "ping pong pals"
    function_registry: FunctionRegistry = function_registry

    def compose(self) -> Iterable[Element]:
        db = get_db()
        session_id = self.request.session.get("session_id")

        try:
            user = get_user_from_session(db=db, session_id=session_id)

            if user is None:
                yield Page(path="/login")
                # This exception should not be needed after redirecting to another page.
                # Just here temporarily to be extra sure.
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="please log in first",
                )
        finally:
            db.close()

        yield Header(id="page-header", text="Games")
        yield NavigationLinks(
            is_logged_in=user is not None,
            is_admin=user.is_admin if user is not None else False,
        )
        yield Header(id="new-game-form-title", text="Register a New Game", level=2)
        yield NewGameForm()
        yield NotificationContainer()


class NewGameForm(Vertical):
    id: str = "new-games-form"

    def compose(self) -> Iterable[Element]:
        yield Paragraph(id="winner-paragraph", text="Select the winner:")
        yield WinnerSelect()
        yield WinnerPointsInput()
        yield Paragraph(id="loser-paragraph", text="Select the loser:")
        yield LoserSelect()
        yield LoserPointsInput()
        yield SubmitGameButton()
