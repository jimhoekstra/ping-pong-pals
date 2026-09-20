from collections.abc import Iterable

from newsflash import Page
from newsflash.models import Element

from ping_pong_pals.database import get_db
from ping_pong_pals.database.crud import revoke_session


class LogoutPage(Page):
    path: str = "/logout"
    page_title: str = "ping pong pals"

    def compose(self) -> Iterable[Element]:
        session_id = self.request.session.get("session_id")

        if session_id is not None:
            db = get_db()
            try:
                revoke_session(db=db, session_id=session_id)
            finally:
                db.close()

        self.request.session.clear()
        yield Page(path="/")
