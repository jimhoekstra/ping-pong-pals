from collections.abc import Iterable

from fastapi import HTTPException, status
from newsflash import Page, FunctionRegistry
from newsflash.elements import Header
from newsflash.models import Element

from ping_pong_pals.database import get_db
from ping_pong_pals.database.crud import (
    get_all_users,
    get_num_played_games,
    get_num_won_games,
    get_user_from_session,
)
from ping_pong_pals.database.models import ProcessedUser
from ping_pong_pals.elements import NavigationLinks

from .elements import PlayersPlot, PlayersTable, PlotWonGamesToggle
from .functions import function_registry


class PlayersPage(Page):
    path: str = "/players"
    page_title: str = "ping pong pals"
    function_registry: FunctionRegistry = function_registry

    def compose(self) -> Iterable[Element]:
        db = get_db()
        session_id = self.request.session.get("session_id")

        try:
            # Ensure user is logged in
            user = get_user_from_session(db=db, session_id=session_id)

            if user is None:
                yield Page(path="/login")
                # This exception should not be needed after redirecting to another page.
                # Just here temporarily to be extra sure.
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="please log in first",
                )

            all_user_ids, all_usernames = get_all_users(db=db)
            num_played_games = [
                get_num_played_games(db=db, user_id=user_id) for user_id in all_user_ids
            ]
            num_won_games = [
                get_num_won_games(db=db, user_id=user_id) for user_id in all_user_ids
            ]

        finally:
            db.close()

        yield Header(id="page-header", text="Players")
        yield NavigationLinks(
            is_logged_in=user is not None,
            is_admin=user.is_admin if user is not None else False,
        )

        processed_users = [
            ProcessedUser(
                rank="t.b.d.",
                username=username,
                games_played=played_games,
                games_won=won_games,
                elo_score="t.b.d.",
            )
            for username, played_games, won_games in zip(
                all_usernames, num_played_games, num_won_games
            )
        ]

        yield Header(id="player-ranking", text="Player Ranking", level=2)
        yield PlayersTable(data=processed_users)

        yield Header(id="num-played-games-header", text="Num Played Games", level=2)
        yield PlotWonGamesToggle()
        yield PlayersPlot(height=50 + 50 * len(processed_users))
