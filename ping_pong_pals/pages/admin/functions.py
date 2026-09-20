from typing import Iterable

from fastapi import Request, HTTPException, status

from newsflash import FunctionRegistry
from newsflash.models import Element
from newsflash.elements import Notification

from ping_pong_pals.database import get_db
from ping_pong_pals.database.crud import (
    create_signup_code,
    delete_signup_code,
    get_all_signup_codes,
    get_user_from_session,
)
from ping_pong_pals.database.models import ProcessedSignupCode

from .elements import (
    NewSignupCodeButton, 
    SignupCodesTable,
    DeleteSignupCodeButton,
    DeleteSignupCodeInput,
)


function_registry = FunctionRegistry()


@function_registry.add(on=NewSignupCodeButton().click())
def create_new_signup_code_callback(request: Request) -> Iterable[Element]:
    db = get_db()
    session_id = request.session.get("session_id")

    try:
        # Ensure user is logged in and is an admin
        user = get_user_from_session(db=db, session_id=session_id)

        if user is None or not user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="unauthorized",
            )

        _ = create_signup_code(db=db)
        all_signup_codes = get_all_signup_codes(db=db)
    finally:
        db.close()

    yield Notification(message="Created code successfully")
    processed_signup_codes = [
        ProcessedSignupCode.from_db_signup_code(signup_code=signup_code)
        for signup_code in all_signup_codes
    ]
    yield SignupCodesTable(data=processed_signup_codes)


@function_registry.add(on=DeleteSignupCodeButton().click())
def delete_signup_code_callback(
    delete_signup_code_input: DeleteSignupCodeInput,
    request: Request,
) -> Iterable[Element]:
    db = get_db()
    session_id = request.session.get("session_id")

    try:
        # Ensure user is logged in and is an admin
        user = get_user_from_session(db=db, session_id=session_id)

        if user is None or not user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="unauthorized",
            )

        success = delete_signup_code(db=db, code=delete_signup_code_input.value)
        if not success:
            raise ValueError()

        all_signup_codes = get_all_signup_codes(db=db)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="code deletion failed",
        )
    finally:
        db.close()

    yield Notification(message="Deleted code successfully")
    yield DeleteSignupCodeInput()
    processed_signup_codes = [
        ProcessedSignupCode.from_db_signup_code(signup_code=signup_code)
        for signup_code in all_signup_codes
    ]
    yield SignupCodesTable(data=processed_signup_codes)
