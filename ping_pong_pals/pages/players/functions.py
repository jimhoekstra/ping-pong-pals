from typing import Iterable

from fastapi import Request, HTTPException, status
from newsflash import FunctionRegistry
from newsflash.models import Element

from ping_pong_pals.database import get_db
from ping_pong_pals.database.crud import get_user_from_session
from ping_pong_pals.database._crud import PlayerDetails

from .elements import PlayersPlot, PlotWonGamesToggle


function_registry = FunctionRegistry()


@function_registry.add(on=[PlayersPlot().revealed(), PlotWonGamesToggle().click()])
def load_players_plot(
    players_plot: PlayersPlot,
    plot_won_games_toggle: PlotWonGamesToggle,
    request: Request,
) -> Iterable[Element]:
    session_id = request.session.get("session_id")
    db = get_db()

    try:
        user = get_user_from_session(db=db, session_id=session_id)

        # Ensure user is logged in
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="please log in first",
            )

        player_details = PlayerDetails.get_for_all_players(
            db=db,
            sort_by="num_games_won"
            if plot_won_games_toggle.checked
            else "num_games_played",
        )
    finally:
        db.close()

    xs = [player.username for player in player_details]
    if plot_won_games_toggle.checked:
        ys = [player.num_games_won for player in player_details]
    else:
        ys = [player.num_games_played for player in player_details]

    fig, ax = players_plot.create_figure()
    try:
        ax.barh(xs, ys, color="#545c92")
        players_plot.set_figure(figure=fig)
    finally:
        players_plot.close_figure(figure=fig)

    yield players_plot
