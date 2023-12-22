from typing import Any
from math import ceil

from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET

from scoreboard.models import Player, Rating
from scoreboard.state import ApplicationState


@login_required
@require_GET
def page(request: HttpRequest) -> HttpResponse:
    '''
    View of all the players, ordered by descending Elo rating, also showing
    the number of games that a player has logged.
    '''
    active_league = ApplicationState.get_active_league(request=request)
    if active_league is None:
        return redirect('leagues')

    context: dict[str, Any] = {'current_view': 'players'}
    all_players = active_league.participants.all().order_by('-current_elo')

    all_players = [{
        'name': player.name,
        'current_elo': player.current_elo,
        'num_games': len(player.won_games.all()) + len(player.lost_games.all())  # type: ignore
    } for player in all_players]

    rated_players = [_player for _player in all_players if _player['num_games'] >= 3]
    unrated_players = [_player for _player in all_players if _player['num_games'] < 3]
    context['rated_players'] = rated_players
    context['unrated_players'] = unrated_players
    context['active_league'] = active_league
    
    return render(request, 'scoreboard/players.html', context=context)


@login_required
@require_GET
def single_player_page(request: HttpRequest, player_name: str, page: int = 1) -> HttpResponse:
    '''
    See a player's game and score history.
    '''
    GAMES_PER_PAGE: int = 10
    context_data: dict[str, Any] = {'current_view': 'players'}

    try:
        player_obj = Player.objects.get(name=player_name)
    except Player.DoesNotExist:
        return render(request, 'scoreboard/bad_request.html', status=400)
    
    total_games_for_player = Rating.objects.filter(player=player_obj).count()
    
    player_scores = Rating.objects.filter(player=player_obj).order_by('-datetime')[
        (page-1)*GAMES_PER_PAGE:page*GAMES_PER_PAGE]
    
    context_data['player_scores'] = player_scores
    context_data['player_obj'] = player_obj
    context_data['pages'] = list(range(1, ceil(total_games_for_player / GAMES_PER_PAGE)+1))
    context_data['current_page'] = page
    context_data['total_games'] = total_games_for_player
    return render(request, 'scoreboard/player.html', context=context_data)
