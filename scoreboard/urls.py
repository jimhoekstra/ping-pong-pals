from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('games', views.games, name='games'),
    path('games/<int:page>', views.games, name='games'),
    path('games/new', views.add_game, name='add-game'),
    path('new-game', views.new_game, name='new-game'),
    path('players', views.players, name='players'),
    path('players/<str:player_name>', views.player, name='player'),
    path('players/<str:player_name>/<int:page>', views.player, name='player')
]
