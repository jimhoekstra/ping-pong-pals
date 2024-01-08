from math import ceil

from scoreboard.views.context import LeagueDependentContext
from scoreboard.models import Rating, Player


def calculate_win_percentage(n_won_games, total_n_games):
    if total_n_games == 0:
        return '--'
    else:
        return str(round(n_won_games / total_n_games * 100))


class PlayersContext(LeagueDependentContext):

    CURRENT_VIEW = 'players'

    def add_all_players(self):
        league = self.get_league()
        all_players = league.participants.all().order_by('-current_elo')

        all_players = [{
            'name': player.name,
            'current_elo': player.current_elo,
            'win_percentage': calculate_win_percentage(len(player.won_games.all()), len(player.won_games.all()) + len(player.lost_games.all())),
            'num_games': len(player.won_games.all()) + len(player.lost_games.all())  # type: ignore
        } for player in all_players]

        rated_players = [_player for _player in all_players if _player['num_games'] >= 3]
        unrated_players = [_player for _player in all_players if _player['num_games'] < 3]
        
        self.context['rated_players'] = rated_players
        self.context['unrated_players'] = unrated_players

        return self

    def add_single_player_info(self, player: Player, page: int, games_per_page: int):
        total_games_for_player = Rating.objects.filter(player=player).count()
        player_scores = Rating.objects.filter(player=player).order_by('-datetime')[
            (page-1)*games_per_page:page*games_per_page]
        
        self.context['player_scores'] = player_scores
        self.context['player_obj'] = player
        self.context['win_percentage'] = calculate_win_percentage(
            len(player.won_games.all()), len(player.won_games.all()) + len(player.lost_games.all()))  # type: ignore
        self.context['pages'] = list(range(1, ceil(total_games_for_player / games_per_page)+1))
        self.context['current_page'] = page
        self.context['total_games'] = total_games_for_player

        return self
