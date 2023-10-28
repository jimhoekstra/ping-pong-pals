from typing import Any
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET, require_POST
from scoreboard.decorators import require_POST_params
from .models import Game, Player, PlayerScore
from .elo import EloRating


@require_GET
def home(request: HttpRequest) -> HttpResponse:
    '''
    Home page view.
    '''
    context_data: dict[str, Any] = {'current_view': 'home'}
    return render(request, 'scoreboard/home.html', context=context_data)


@login_required
@require_GET
def games(request: HttpRequest) -> HttpResponse:
    '''
    View of the most recent 20 games that have been played.
    The page also includes a form for submitting a new game.
    '''
    context: dict[str, Any] = {'current_view': 'games'}
    context['all_players'] = Player.objects.all()
    context['all_games'] = Game.objects.all().order_by('-date')[:20]
    return render(request, 'scoreboard/games.html', context=context)


@login_required
@require_POST
@require_POST_params(['winner', 'loser', 'winner-points', 'loser-points'])
def new_game(request: HttpRequest) -> HttpResponse:
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


@login_required
@require_GET
def players(request: HttpRequest) -> HttpResponse:
    '''
    View of all the players, ordered by descending Elo rating, also showing
    the number of games that a player has logged.
    '''
    context: dict[str, Any] = {'current_view': 'players'}
    all_players = Player.objects.all().order_by('-current_elo')

    all_players = [{
        'name': player.name,
        'current_elo': player.current_elo,
        'num_games': len(player.won_games.all()) + len(player.lost_games.all())  # type: ignore
    } for player in all_players]
    context['all_players'] = all_players
    
    return render(request, 'scoreboard/players.html', context=context)


@login_required
@require_GET
def player(request: HttpRequest, player_name: str) -> HttpResponse:
    '''
    See a player's game and score history.
    '''
    context_data: dict[str, Any] = {'current_view': 'players'}

    try:
        player_obj = Player.objects.get(name=player_name)
    except Player.DoesNotExist:
        return render(request, 'scoreboard/bad_request.html', status=400)
    
    player_scores = PlayerScore.objects.filter(player=player_obj).order_by('-datetime')
    context_data['player_scores'] = player_scores
    context_data['player_name'] = player_obj.name
    return render(request, 'scoreboard/player.html', context=context_data)
