from collections.abc import Iterable

from fastapi import HTTPException, Request, status
from newsflash import FunctionRegistry, Page
from newsflash.models import Element
from sqlalchemy.exc import IntegrityError

from ping_pong_pals.database import get_db
from ping_pong_pals.database.crud import (
    SignupCodeValidationError,
    create_user,
    login_user_and_create_session,
)

from .elements import (
    UsernameInput,
    PasswordInput,
    PasswordConfirmationInput,
    SignupCodeInput,
    RegisterButton,
)


function_registry = FunctionRegistry()


@function_registry.add(on=RegisterButton().click())
def register_user(
    username_input: UsernameInput,
    password_input: PasswordInput,
    password_confirmation_input: PasswordConfirmationInput,
    signup_code_input: SignupCodeInput,
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
