from typing import Any
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET, require_POST
from elo.decorators import require_POST_params
from .models import Game, Player
from .elo import EloRating


@require_GET
def home(request: HttpRequest) -> HttpResponse:
    return render(request, 'elo/home.html')


@login_required
@require_GET
def games(request: HttpRequest) -> HttpResponse:
    context: dict[str, Any] = {'current_view': 'games'}
    context['all_players'] = Player.objects.all()
    context['all_games'] = Game.objects.all().order_by('-date')[:20]
    return render(request, 'elo/games.html', context=context)


@login_required
@require_POST
@require_POST_params(['winner', 'loser', 'winner-points', 'loser-points'])
def new_game(request: HttpRequest) -> HttpResponse:   
    winner_id = int(request.POST['winner'])
    loser_id = int(request.POST['loser'])
    if winner_id == loser_id:
        return redirect('games')
    
    winner_obj = Player.objects.get(pk=winner_id)
    loser_obj = Player.objects.get(pk=loser_id)
    elo_rating = EloRating(winner=winner_obj, loser=loser_obj)

    new_game = Game(
        winner=winner_obj,
        loser=loser_obj,
        winner_points=request.POST['winner-points'],
        loser_points=request.POST['loser-points'],
        winner_elo_before=winner_obj.current_elo,
        winner_elo_after=elo_rating.get_new_winner_rating(),
        loser_elo_before=loser_obj.current_elo,
        loser_elo_after=elo_rating.get_new_loser_rating()
    )
    new_game.save()
    elo_rating.commit_scores()

    return redirect('games')


@login_required
@require_GET
def players(request: HttpRequest) -> HttpResponse:
    context: dict[str, Any] = {'current_view': 'players'}
    all_players = Player.objects.all().order_by('-current_elo')

    all_players = [{
        'name': player.name,
        'current_elo': player.current_elo,
        'num_games': len(player.won_games.all()) + len(player.lost_games.all())  # type: ignore
    } for player in all_players]
    context['all_players'] = all_players
    
    return render(request, 'elo/players.html', context=context)
