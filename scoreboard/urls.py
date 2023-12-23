from django.urls import path

from scoreboard.views import home
from scoreboard.views import leagues
from scoreboard.views import games
from scoreboard.views import players


home_urlpatterns = [
    path('', home.page, name='home'),
]

leagues_urlpatterns = [
    path('leagues', leagues.views.page, name='leagues'),
    path('leagues/activate', leagues.views.activate_league, name='activate-league'),
    path('leagues/deactivate', leagues.views.deactivate_league, name='deactivate-league'),
    path('leagues/new', leagues.views.new_league_page, name='new-league-page'),
    path('leagues/submit', leagues.views.submit_new_league, name='submit-new-league'),
    path('leagues/<slug:league>', leagues.views.detail_page, name='league-detail'),
]

games_urlpatterns = [
    path('games', games.views.select_league_page, name='games'),
    path('leagues/<slug:league>/games', games.views.games_page, name='games-for-league'),
    path('leagues/<slug:league>/games/<int:page>', games.views.games_page, name='games-page'),
    path('leagues/<slug:league>/games/new', games.views.new_game_page, name='add-game'),
    path('leagues/<slug:league>/games/submit', games.views.submit_new_game, name='new-game'),
]

players_urlpatterns = [
    path('players', players.views.select_league_page, name='players'),
    path('leagues/<slug:league>/players', players.views.page, name='players-for-league'),
    path('leagues/<slug:league>/players/<str:player_name>', players.views.single_player_page, name='player'),
    path('leagues/<slug:league>/players/<str:player_name>/<int:page>', players.views.single_player_page, name='player'),
]


urlpatterns = (
    home_urlpatterns +
    leagues_urlpatterns +
    games_urlpatterns +
    players_urlpatterns
)
