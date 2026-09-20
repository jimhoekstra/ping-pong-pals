from newsflash import NewsflashApp
from starlette.middleware.sessions import SessionMiddleware

from ping_pong_pals.database import create_all
from ping_pong_pals.pages import (
    AdminPage,
    GamesPage,
    HomePage,
    LoginPage,
    LogoutPage,
    PlayersPage,
    RegisterPage,
)

create_all()


app = NewsflashApp(
    pages=[
        HomePage,
        LoginPage,
        LogoutPage,
        RegisterPage,
        GamesPage,
        PlayersPage,
        AdminPage,
    ]
)
app.add_middleware(SessionMiddleware, secret_key="very-secret")
