from typing import Any

from scoreboard.models import League
from scoreboard.views.context import GenericContext


class LeagueContext(GenericContext):

    CURRENT_VIEW: str = 'leagues'

    PAGE_TITLE_KEY: str = 'page_title'
    ALL_LEAGUES_KEY: str = 'all_leagues'
    NEXT_PAGE_URL_NAME_KEY: str = 'next_page_url_name'

    def set_page_title(self, title: str):
        self.context[self.PAGE_TITLE_KEY] = title
        return self
    
    def set_next_page_url_name(self, next_page_url_name: str):
        self.context[self.NEXT_PAGE_URL_NAME_KEY] = next_page_url_name
        return self
    
    def add_all_leagues_info(self):
        player = self.request.user.player  # type: ignore

        all_leagues = player.leagues.all()

        self.context[self.ALL_LEAGUES_KEY] = [{
            'league': league,
            'n_participants': league.participants.count(),
            'n_games': league.games.count()  # type: ignore
        } for league in all_leagues]

        return self
