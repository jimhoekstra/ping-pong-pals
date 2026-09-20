from newsflash.elements import Input, Button
from newsflash.elements import PasswordInput as BasePasswordInput


class UsernameInput(Input):
    id: str = "username-input"
    placeholder: str = "username"


class PasswordInput(BasePasswordInput):
    id: str = "password-input"
    placeholder: str = "password"


class LoginButton(Button):
    id: str = "login-button"
    label: str = "Login"
