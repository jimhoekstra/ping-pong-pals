from collections.abc import Iterable
from typing import Annotated

from fastapi import HTTPException, Request, status
from newsflash import FunctionRegistry, Page
from newsflash.elements import (
    Button,
    Header,
    Input,
    NotificationContainer,
    PasswordInput,
)
from newsflash.models import ID, Element

from ping_pong_pals.database import get_db
from ping_pong_pals.database.crud import login_user_and_create_session
from ping_pong_pals.elements import NavigationLinks

function_registry = FunctionRegistry()


@function_registry.add(on=Button(id="login-button").click())
def login_user(
    username_input: Annotated[Input, ID("username-input")],
    password_input: Annotated[PasswordInput, ID("password-input")],
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

    yield Page(path="/")


class LoginPage(Page):
    path: str = "/login"
    page_title: str = "ping pong pals"
    function_registry: FunctionRegistry = function_registry

    def compose(self) -> Iterable[Element]:
        yield Header(id="page-header", text="Login")
        yield NavigationLinks(is_logged_in=False, is_admin=False)
        yield Header(id="login-form-header", text="Login Form", level=2)
        yield from _empty_inputs()
        yield Button(id="login-button", label="Login")
        yield NotificationContainer()


def _empty_inputs() -> Iterable[Element]:
    yield Input(id="username-input", placeholder="username")
    yield PasswordInput(id="password-input", placeholder="password")
