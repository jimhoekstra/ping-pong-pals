from typing import Iterable

from newsflash import Page, FunctionRegistry
from newsflash.models import Element
from newsflash.elements import (
    Header,
    Paragraph,
    NotificationContainer,
)

from ping_pong_pals.elements import NavigationLinks

from .elements import (
    UsernameInput,
    PasswordInput,
    PasswordConfirmationInput,
    SignupCodeInput,
    RegisterButton,
)
from .functions import function_registry


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

        yield UsernameInput()
        yield PasswordInput()
        yield PasswordConfirmationInput()
        yield SignupCodeInput()
        yield RegisterButton()

        yield NotificationContainer()
