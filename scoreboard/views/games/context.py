from math import ceil

from scoreboard.views.context import LeagueDependentContext
from scoreboard.models import Game


class GamesContext(LeagueDependentContext):
    
    CURRENT_VIEW = 'games'

    TOTAL_NUMBER_OF_GAMES_KEY: str = 'total_number_of_games'
    ALL_PLAYERS_KEY: str = 'all_players'

    def add_total_number_of_games(self):
        total_number_of_games = Game.objects.filter(league=self.get_league()).count()
        self.context[self.TOTAL_NUMBER_OF_GAMES_KEY] = total_number_of_games
        return self

    def add_games_for_page(self, page: int, games_per_page: int):
        total_number_of_games = Game.objects.filter(league=self.get_league()).count()

        self.context['all_games'] = Game.objects.filter(
            league=self.get_league()).order_by('-date')[(page-1)*games_per_page:(page)*games_per_page]
        
        self.context['pages'] = list(range(1, ceil(total_number_of_games / games_per_page)+1))
        self.context['current_page'] = page
        return self

    def add_all_players(self):
        self.context[self.ALL_PLAYERS_KEY] = self.get_league().participants.all()
        return self
