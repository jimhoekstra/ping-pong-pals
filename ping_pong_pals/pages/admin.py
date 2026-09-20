from collections.abc import Iterable

from fastapi import HTTPException, Request, status
from newsflash import FunctionRegistry, Page
from newsflash.elements import (
    Button,
    Header,
    Input,
    Notification,
    NotificationContainer,
    Table,
    Vertical,
)
from newsflash.models import Element

from ping_pong_pals.database import get_db
from ping_pong_pals.database.crud import (
    create_signup_code,
    delete_signup_code,
    get_all_signup_codes,
    get_user_from_session,
)
from ping_pong_pals.database.models import ProcessedSignupCode, SignupCode
from ping_pong_pals.elements import NavigationLinks

function_registry = FunctionRegistry()


class NewSignupCodeButton(Button):
    id: str = "new-signup-code-button"
    label: str = "Create New Signup Code"


class SignupCodesTable(Table):
    id: str = "signup-codes-table"


class DeleteSignupCodeInput(Input):
    id: str = "delete-signup-code-input"
    placeholder: str = "signup code to delete"


class DeleteSignupCodeButton(Button):
    id: str = "delete-signup-code-button"
    label: str = "Delete Signup Code"


@function_registry.add(on=NewSignupCodeButton().click())
def create_new_signup_code_callback(request: Request) -> Iterable[Element]:
    db = get_db()
    session_id = request.session.get("session_id")

    try:
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
    processed_signup_codes = _db_to_processed_signup_codes(
        signup_codes=all_signup_codes
    )
    yield SignupCodesTable(data=processed_signup_codes)


@function_registry.add(on=DeleteSignupCodeButton().click())
def delete_signup_code_callback(
    delete_signup_code_input: DeleteSignupCodeInput,
    request: Request,
) -> Iterable[Element]:
    db = get_db()
    session_id = request.session.get("session_id")

    try:
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
    processed_signup_codes = _db_to_processed_signup_codes(
        signup_codes=all_signup_codes
    )
    yield SignupCodesTable(data=processed_signup_codes)


class AdminPage(Page):
    path: str = "/admin"
    page_title: str = "ping pong pals"
    function_registry: FunctionRegistry = function_registry

    def compose(self) -> Iterable[Element]:
        db = get_db()
        session_id = self.request.session.get("session_id")

        try:
            user = get_user_from_session(db=db, session_id=session_id)

            if user is None or not user.is_admin:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="unauthorized",
                )

            all_signup_codes = get_all_signup_codes(db=db)
        finally:
            db.close()

        yield Header(id="page-title", text="Admin")
        yield NavigationLinks(
            is_logged_in=user is not None,
            is_admin=user.is_admin if user is not None else False,
        )

        yield Header(id="new-signup-code-header", text="Create a Code", level=2)
        yield NewSignupCodeButton()

        yield Header(id="all-signup-codes-header", text="All codes", level=2)
        processed_signup_codes = _db_to_processed_signup_codes(
            signup_codes=all_signup_codes
        )
        yield SignupCodesTable(data=processed_signup_codes)

        yield Header(id="delete-signup-code-header", text="Delete a Code", level=2)
        yield DeleteSignupCodeForm()
        yield NotificationContainer()


class NewSignupCodeForm(Vertical):
    id: str = "new-signup-code-form"

    def compose(self) -> Iterable[Element]:
        yield NewSignupCodeButton()


class DeleteSignupCodeForm(Vertical):
    id: str = "delete-signup-code-form"

    def compose(self) -> Iterable[Element]:
        yield DeleteSignupCodeInput()
        yield DeleteSignupCodeButton()


def _db_to_processed_signup_codes(
    signup_codes: list[SignupCode],
) -> list[ProcessedSignupCode]:
    processed_signup_codes = [
        ProcessedSignupCode.from_db_signup_code(signup_code=signup_code)
        for signup_code in signup_codes
    ]
    return processed_signup_codes
