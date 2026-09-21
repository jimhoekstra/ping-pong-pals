from collections.abc import Iterable

from newsflash import FunctionRegistry, Page
from newsflash.elements import (
    Header,
    NotificationContainer,
    Paragraph,
)
from newsflash.models import Element

from ping_pong_pals.elements import NavigationLinks

from .elements import UsernameInput, PasswordInput, LoginButton
from .functions import function_registry


class LoginPage(Page):
    path: str = "/login"
    page_title: str = "ping pong pals"
    function_registry: FunctionRegistry = function_registry

    def compose(self) -> Iterable[Element]:
        yield Header(id="page-header", text="Login")
        yield NavigationLinks(is_logged_in=False, is_admin=False)

        yield Header(id="login-form-header", text="Login Form", level=2)
        yield Paragraph(id="login-form-paragraph", text="Enter your login credentials below to log in.")
        yield UsernameInput()
        yield PasswordInput()
        yield LoginButton()
        
        yield NotificationContainer()
