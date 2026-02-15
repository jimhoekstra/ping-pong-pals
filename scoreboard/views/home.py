from typing import Any
from datetime import datetime
from math import floor

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_GET
from django.utils import timezone

from scoreboard.models import Game, Player


@require_GET
def page(request: HttpRequest) -> HttpResponse:
    '''
    Home page view.
    '''
    context_data: dict[str, Any] = {'current_view': 'home'}
    now = timezone.now()

    game_count = Game.objects.count()
    game_count_this_month = Game.objects.filter(
        date__gte=datetime(year=now.year, month=now.month, day=1)).count()
    player_count = Player.objects.count()

    if not request.user.is_authenticated:
        game_count = floor(game_count / 10) * 10
        game_count_this_month = floor(game_count_this_month / 10) * 10
        player_count = floor(player_count / 10) * 10

    context_data['user_is_authenticated'] = request.user.is_authenticated
    context_data['total_number_of_games'] = game_count
    context_data['total_number_of_players'] = player_count
    context_data['number_of_games_this_month'] = game_count_this_month

    return render(request, 'scoreboard/home/page.html', context=context_data)


def not_implemented(request: HttpRequest) -> HttpResponse:
    '''
    Page to show when the users requests functionality that is not yet implemented.
    '''
    return render(request, 'scoreboard/generic/not_implemented.html')
