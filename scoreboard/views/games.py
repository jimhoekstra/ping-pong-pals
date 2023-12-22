from typing import Any
from math import ceil

from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET, require_POST

from scoreboard.decorators import require_POST_params
from scoreboard.models import Game, Player
from scoreboard.elo import EloRating
from scoreboard.state import ApplicationState


@login_required
@require_GET
def games_page(request: HttpRequest, page: int = 1) -> HttpResponse:
    '''
    View of the most recent 20 games that have been played.
    The page also includes a form for submitting a new game.
    '''
    active_league = ApplicationState.get_active_league(request=request)
    if active_league is None:
        return redirect('leagues')

    GAMES_PER_PAGE: int = 10
    total_number_of_games = Game.objects.filter(league=active_league).count()

    if page > ceil(total_number_of_games / GAMES_PER_PAGE) and total_number_of_games != 0:
        return redirect('games')

    context: dict[str, Any] = {'current_view': 'games'}
    context['all_games'] = Game.objects.filter(
        league=active_league).order_by('-date')[(page-1)*GAMES_PER_PAGE:(page)*GAMES_PER_PAGE]
    
    context['pages'] = list(range(1, ceil(total_number_of_games / GAMES_PER_PAGE)+1))
    context['current_page'] = page
    context['total_number_of_games'] = total_number_of_games
    context['active_league'] = active_league
    return render(request, 'scoreboard/games.html', context=context)


@login_required
@require_GET
def new_game_page(request: HttpRequest) -> HttpResponse:
    context: dict[str, Any] = {'current_view': 'games'}
    context['all_players'] = Player.objects.all()
    return render(request, 'scoreboard/add_game.html', context=context)


@login_required
@require_POST
@require_POST_params(['winner', 'loser', 'winner-points', 'loser-points'])
def submit_new_game(request: HttpRequest) -> HttpResponse:
    '''
    Endpoint for submitting the results of a new game, to be added to the database.
    '''
    winner_id = int(request.POST['winner'])
    loser_id = int(request.POST['loser'])

    try:
        winner_points = int(request.POST['winner-points'])
        loser_points = int(request.POST['loser-points'])
    except ValueError:
        return render(request, 'scoreboard/bad_request.html', status=400)

    if winner_id == loser_id:
        return redirect('games')
    
    winner_obj = Player.objects.get(pk=winner_id)
    loser_obj = Player.objects.get(pk=loser_id)
    elo_rating = EloRating(winner=winner_obj, loser=loser_obj)

    new_game = Game(
        winner=winner_obj,
        loser=loser_obj,
        winner_points=winner_points,
        loser_points=loser_points
    )
    new_game.save()
    elo_rating.commit_scores(game=new_game)

    return redirect('games')
