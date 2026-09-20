from collections.abc import Iterable

from newsflash.elements import Horizontal, Link
from newsflash.models import Element


class NavigationLinks(Horizontal):
    id: str = "navigation-links-row"
    justify: bool = False
    is_logged_in: bool = False
    is_admin: bool = False

    def compose(self) -> Iterable[Element]:
        yield Link(id="link-to-home", href="/", text="Home")

        if not self.is_logged_in:
            yield Link(id="link-to-login", href="/login", text="Login")
            yield Link(id="link-to-register", href="/register", text="Register")

        if self.is_logged_in:
            yield Link(id="link-to-games", href="/games", text="Games")
            yield Link(id="link-to-players", href="/players", text="Players")

        if self.is_admin:
            yield Link(id="link-to-admin", href="/admin", text="Admin")

        if self.is_logged_in:
            yield Link(id="link-to-logout", href="/logout", text="Logout")
