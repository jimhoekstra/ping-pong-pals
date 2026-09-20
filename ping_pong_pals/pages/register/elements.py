from newsflash.elements import (
    Input,
    PasswordInput as BasePasswordInput,
    Button,
)


class UsernameInput(Input):
    id: str = "username-input"
    placeholder: str = "username"


class PasswordInput(BasePasswordInput):
    id: str = "password-input"
    placeholder: str = "password"


class PasswordConfirmationInput(BasePasswordInput):
    id: str = "password-confirmation-input"
    placeholder: str = "confirm password"


class SignupCodeInput(Input):
    id: str = "signup-code-input"
    placeholder: str = "signup code"


class RegisterButton(Button):
    id: str = "register-button"
    label: str = "Register"
