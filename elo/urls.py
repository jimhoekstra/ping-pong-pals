from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('games', views.games, name='games'),
    path('new-game', views.new_game, name='new-game'),
    path('players', views.players, name='players')
]
