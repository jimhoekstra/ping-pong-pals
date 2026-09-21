from typing import Iterable

from newsflash.models import Element
from newsflash.elements import (
    Button,
    Input,
    Table,
    Vertical,
)


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


class NewSignupCodeForm(Vertical):
    id: str = "new-signup-code-form"

    def compose(self) -> Iterable[Element]:
        yield NewSignupCodeButton()


class DeleteSignupCodeForm(Vertical):
    id: str = "delete-signup-code-form"

    def compose(self) -> Iterable[Element]:
        yield DeleteSignupCodeInput()
        yield DeleteSignupCodeButton()
