from typing import Any
from math import ceil
from datetime import timedelta
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET, require_POST
from django.utils import timezone
from scoreboard.decorators import require_POST_params
from .models import Game, Player, PlayerScore
from .elo import EloRating


@require_GET
def home(request: HttpRequest) -> HttpResponse:
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


@login_required
@require_GET
def games(request: HttpRequest, page: int = 1) -> HttpResponse:
    '''
    View of the most recent 20 games that have been played.
    The page also includes a form for submitting a new game.
    '''
    GAMES_PER_PAGE: int = 10
    total_number_of_games = Game.objects.count()

    if page > ceil(total_number_of_games / GAMES_PER_PAGE):
        return redirect('games')

    context: dict[str, Any] = {'current_view': 'games'}
    context['all_games'] = Game.objects.all().order_by('-date')[(page-1)*GAMES_PER_PAGE:(page)*GAMES_PER_PAGE]
    context['pages'] = list(range(1, ceil(total_number_of_games / GAMES_PER_PAGE)+1))
    context['current_page'] = page
    return render(request, 'scoreboard/games.html', context=context)


@login_required
@require_GET
def add_game(request: HttpRequest) -> HttpResponse:
    context: dict[str, Any] = {'current_view': 'games'}
    context['all_players'] = Player.objects.all()
    return render(request, 'scoreboard/add_game.html', context=context)


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

    rated_players = [_player for _player in all_players if _player['num_games'] >= 3]
    unrated_players = [_player for _player in all_players if _player['num_games'] < 3]
    context['rated_players'] = rated_players
    context['unrated_players'] = unrated_players
    
    return render(request, 'scoreboard/players.html', context=context)


@login_required
@require_GET
def player(request: HttpRequest, player_name: str, page: int = 1) -> HttpResponse:
    '''
    See a player's game and score history.
    '''
    GAMES_PER_PAGE: int = 10
    context_data: dict[str, Any] = {'current_view': 'players'}

    try:
        player_obj = Player.objects.get(name=player_name)
    except Player.DoesNotExist:
        return render(request, 'scoreboard/bad_request.html', status=400)
    
    total_games_for_player = PlayerScore.objects.filter(player=player_obj).count()
    
    player_scores = PlayerScore.objects.filter(player=player_obj).order_by('-datetime')[
        (page-1)*GAMES_PER_PAGE:page*GAMES_PER_PAGE]
    
    context_data['player_scores'] = player_scores
    context_data['player_obj'] = player_obj
    context_data['pages'] = list(range(1, ceil(total_games_for_player / GAMES_PER_PAGE)+1))
    context_data['current_page'] = page
    context_data['total_games'] = total_games_for_player
    return render(request, 'scoreboard/player.html', context=context_data)
