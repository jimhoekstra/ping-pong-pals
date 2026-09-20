from collections.abc import Iterable
from typing import Annotated

from fastapi import HTTPException, Request, status
from newsflash import FunctionRegistry, Page
from newsflash.elements import (
    Button,
    Header,
    Input,
    NotificationContainer,
    Paragraph,
    PasswordInput,
)
from newsflash.models import ID, Element
from sqlalchemy.exc import IntegrityError

from ping_pong_pals.database import get_db
from ping_pong_pals.database.crud import (
    SignupCodeValidationError,
    create_user,
    login_user_and_create_session,
)
from ping_pong_pals.elements import NavigationLinks

function_registry = FunctionRegistry()


@function_registry.add(on=Button(id="register-button").click())
def register_user(
    username_input: Annotated[Input, ID("username-input")],
    password_input: Annotated[PasswordInput, ID("password-input")],
    password_confirmation_input: Annotated[
        PasswordInput, ID("password-confirmation-input")
    ],
    signup_code_input: Annotated[Input, ID("signup-code-input")],
    request: Request,
) -> Iterable[Element]:
    if username_input.value == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="username is not filled in",
        )
    if len(password_input.value) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="password needs to be at least 8 characters",
        )
    if password_input.value != password_confirmation_input.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="passwords don't match",
        )

    db = get_db()
    try:
        create_user(
            db=db,
            username=username_input.value,
            password=password_input.value,
            signup_code=signup_code_input.value,
        )

        session = login_user_and_create_session(
            db=db,
            username=username_input.value,
            password=password_input.value,
        )

        assert session is not None
        request.session["session_id"] = session.id

        yield Page(path="/")
    except SignupCodeValidationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="signup code is not valid",
        )
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="this username already exists, please pick a different one",
        )
    finally:
        db.close()


class RegisterPage(Page):
    path: str = "/register"
    page_title: str = "ping pong pals"
    function_registry: FunctionRegistry = function_registry

    def compose(self) -> Iterable[Element]:
        yield Header(id="page-header", text="Register")
        yield NavigationLinks(is_logged_in=False, is_admin=False)
        yield Header(id="register-form-header", text="Registration Form", level=2)
        yield Paragraph(
            id="register-form-paragraph",
            text=(
                "Note: you will a signup code to register. Please ask your site "
                "administrator if you don't have one yet."
            ),
        )
        yield from _empty_inputs()
        yield Button(id="register-button", label="Register")
        yield NotificationContainer()


def _empty_inputs() -> Iterable[Element]:
    yield Input(id="username-input", placeholder="username")
    yield PasswordInput(id="password-input", placeholder="password")
    yield PasswordInput(
        id="password-confirmation-input", placeholder="confirm password"
    )
    yield Input(id="signup-code-input", placeholder="signup code")
