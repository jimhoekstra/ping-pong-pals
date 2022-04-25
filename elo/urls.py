from django.urls import path
from .views import index, GamesView, PlayersView


urlpatterns = [
    path('', index, name='index'),
    path('games/', GamesView.as_view(), name='games'),
    path('players/', PlayersView.as_view(), name='players')
]
