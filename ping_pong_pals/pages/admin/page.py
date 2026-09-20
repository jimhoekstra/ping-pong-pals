from typing import Iterable

from fastapi import HTTPException, status

from newsflash import Page, FunctionRegistry
from newsflash.models import Element
from newsflash.elements import (
    Header,
    NotificationContainer,
)

from ping_pong_pals.database import get_db
from ping_pong_pals.database.crud import (
    get_all_signup_codes,
    get_user_from_session,
)
from ping_pong_pals.elements import NavigationLinks
from ping_pong_pals.database.models import ProcessedSignupCode

from .functions import function_registry
from .elements import (
    NewSignupCodeButton,
    SignupCodesTable,
    DeleteSignupCodeForm,
)


class AdminPage(Page):
    path: str = "/admin"
    page_title: str = "ping pong pals"
    function_registry: FunctionRegistry = function_registry

    def compose(self) -> Iterable[Element]:
        db = get_db()
        session_id = self.request.session.get("session_id")

        try:
            # Ensure user is logged in and is an admin
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
        processed_signup_codes = [
            ProcessedSignupCode.from_db_signup_code(signup_code=signup_code)
            for signup_code in all_signup_codes
        ]
        yield SignupCodesTable(data=processed_signup_codes)

        yield Header(id="delete-signup-code-header", text="Delete a Code", level=2)
        yield DeleteSignupCodeForm()
        yield NotificationContainer()
