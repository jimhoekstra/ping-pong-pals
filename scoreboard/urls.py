from django.urls import path

from scoreboard.views import home
from scoreboard.views import leagues
from scoreboard.views import games
from scoreboard.views import players


home_urlpatterns = [
    path('', home.page, name='home'),
]

leagues_urlpatterns = [
    path('leagues', leagues.page, name='leagues'),
    path('leagues/activate', leagues.activate_league, name='activate-league'),
    path('leagues/new', leagues.new_league_page, name='new-league-page'),
    path('leagues/submit', leagues.submit_new_league, name='submit-new-league'),
]

games_urlpatterns = [
    path('games', games.games_page, name='games'),
    path('games/<int:page>', games.games_page, name='games'),
    path('games/new', games.new_game_page, name='add-game'),
    path('games/submit', games.submit_new_game, name='new-game'),
]

players_urlpatterns = [
    path('players', players.page, name='players'),
    path('players/<str:player_name>', players.single_player_page, name='player'),
    path('players/<str:player_name>/<int:page>', players.single_player_page, name='player'),
]


urlpatterns = (
    home_urlpatterns +
    leagues_urlpatterns +
    games_urlpatterns +
    players_urlpatterns
)
