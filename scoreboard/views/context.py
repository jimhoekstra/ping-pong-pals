from typing import Any

from django.http import HttpRequest

from scoreboard.models import League
from scoreboard.state import ApplicationState


class GenericContext:

    request: HttpRequest
    context: dict[str, Any]

    CURRENT_VIEW: str

    CURRENT_VIEW_KEY: str = 'current_view'
    LOGGED_IN_PLAYER_KEY: str = 'logged_in_player'
    CURRENT_LEAGUE_KEY: str = 'current_league'

    def __init__(self, request: HttpRequest) -> None:
        self.request = request
        self.context = {self.CURRENT_VIEW_KEY: self.CURRENT_VIEW}

    def override_current_view(self, current_view: str):
        self.context[self.CURRENT_VIEW_KEY] = current_view
        return self

    def add_logged_in_player(self):
        self.context[self.LOGGED_IN_PLAYER_KEY] = self.request.user.player  # type: ignore
        return self
    
    def add_current_league(self, league: League):
        self.context[self.CURRENT_LEAGUE_KEY] = league
        return self
    
    def add_current_league_from_app_state_if_exists(self):
        active_league = ApplicationState.get_active_league(request=self.request)
        if active_league is None:
            return self
        return self.add_current_league(league=active_league)
    
    def add_current_league_from_app_state(self):
        active_league = ApplicationState.get_active_league(request=self.request)
        if active_league is None:
            raise ValueError('league has not been set in application state')
        return self.add_current_league(league=active_league)

    def as_context_dict(self) -> dict[str, Any]:
        return self.context


class LeagueDependentContext(GenericContext):

    league: League | None = None

    def set_league(self, league: League):
        self.league = league
        return self

    def get_league(self) -> League:
        if self.league is None:
            raise ValueError('league has not been set in a league dependent context')
        return self.league

    def add_current_league(self, league: League):
        self.league = league
        return super().add_current_league(league)
