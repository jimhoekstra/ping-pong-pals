from typing import Any
from datetime import timedelta

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

    context_data['user_is_authenticated'] = request.user.is_authenticated
    context_data['total_number_of_games'] = Game.objects.count()
    context_data['total_number_of_players'] = Player.objects.count()
    seven_days_ago = timezone.now() - timedelta(days=7)
    context_data['number_of_games_in_last_seven_days'] = Game.objects.filter(date__gte=seven_days_ago).count()
    return render(request, 'scoreboard/home.html', context=context_data)
