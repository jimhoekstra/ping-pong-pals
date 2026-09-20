from collections.abc import Iterable

from fastapi import HTTPException, status
from newsflash import FunctionRegistry, Page
from newsflash.elements import (
    Header,
    NotificationContainer,
)
from newsflash.models import Element

from ping_pong_pals.elements import NavigationLinks
from ping_pong_pals.database import get_db
from ping_pong_pals.database.crud import get_user_from_session

from .elements import NewGameForm
from .functions import function_registry


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
