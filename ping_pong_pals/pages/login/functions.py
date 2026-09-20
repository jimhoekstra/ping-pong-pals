from collections.abc import Iterable

from fastapi import HTTPException, Request, status
from newsflash import FunctionRegistry, Page
from newsflash.models import Element

from ping_pong_pals.database import get_db
from ping_pong_pals.database.crud import login_user_and_create_session

from .elements import UsernameInput, PasswordInput, LoginButton

function_registry = FunctionRegistry()


@function_registry.add(on=LoginButton().click())
def login_user(
    username_input: UsernameInput,
    password_input: PasswordInput,
    request: Request,
) -> Iterable[Element]:
    if username_input.value == "" or password_input.value == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="username and/or password is not filled in",
        )

    db = get_db()
    try:
        session = login_user_and_create_session(
            db=db,
            username=username_input.value,
            password=password_input.value,
        )

        if session is None:
            # Authentication was unsuccessful
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="username and/or password is incorrect",
            )

        request.session["session_id"] = session.id
    finally:
        db.close()

    # Redirect to home page
    yield Page(path="/")
