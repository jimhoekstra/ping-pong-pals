from collections.abc import Iterable

from newsflash import Page
from newsflash.elements import Header, Paragraph
from newsflash.models import Element

from ping_pong_pals.database import get_db
from ping_pong_pals.database.crud import get_user_from_session
from ping_pong_pals.elements import NavigationLinks


class HomePage(Page):
    path: str = "/"
    page_title: str = "ping pong pals"

    def compose(self) -> Iterable[Element]:
        db = get_db()
        session_id = self.request.session.get("session_id")

        try:
            user = get_user_from_session(db=db, session_id=session_id)
        finally:
            db.close()

        username = f", {user.username}" if user is not None else ""

        yield Header(id="title", text="Ping Pong Pals")
        yield NavigationLinks(
            is_logged_in=user is not None,
            is_admin=user.is_admin if user is not None else False,
        )
        yield Header(id="welcome-header", text=f"Welcome{username}!", level=2)
        yield Paragraph(
            id="introduction",
            text="Enjoy your daily serve of friendly competition.",
        )
