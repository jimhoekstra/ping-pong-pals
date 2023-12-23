from typing import Any
from math import ceil

from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET, require_POST

from scoreboard.decorators import require_POST_params
from scoreboard.models import Game, Player, League
from scoreboard.elo import EloRating
from scoreboard.state import ApplicationState
from scoreboard.views.games.context import GamesContext
from scoreboard.views.leagues.context import LeagueContext


@login_required
@require_GET
def select_league_page(request: HttpRequest) -> HttpResponse:
    active_league = ApplicationState.get_active_league(request=request)
    if active_league is not None:
        return redirect('games-for-league', league=active_league.slug)
    
    context = (LeagueContext(request=request)
                .override_current_view('games')
                .set_page_title('Games')
                .set_next_page_url_name('games-for-league')
                .add_current_league_from_app_state_if_exists()
                .add_logged_in_player()
                .add_all_leagues_info()
                .as_context_dict())

    return render(request, 'scoreboard/leagues.html', context=context)


@login_required
@require_GET
def games_page(request: HttpRequest, league: str, page: int = 1) -> HttpResponse:
    '''
    View of the most recent games that have been played.
    '''
    league_obj = League.objects.get(slug=league)
    GAMES_PER_PAGE: int = 10

    total_number_of_games = Game.objects.filter(league=league_obj).count()
    if page > ceil(total_number_of_games / GAMES_PER_PAGE) and total_number_of_games != 0:
        return redirect('games')
    
    context: dict[str, Any] = (GamesContext(request=request)
                                .add_current_league(league=league_obj)
                                .add_total_number_of_games()
                                .add_games_for_page(page=page, games_per_page=GAMES_PER_PAGE)
                                .as_context_dict())
    
    return render(request, 'scoreboard/games.html', context=context)


@login_required
@require_GET
def new_game_page(request: HttpRequest, league: str) -> HttpResponse:
    '''
    Page with a form for submitting a new game.
    '''
    league_obj = League.objects.get(slug=league)

    context: dict[str, Any] = (GamesContext(request=request)
                                .add_current_league(league=league_obj)
                                .add_all_players()
                                .as_context_dict())

    return render(request, 'scoreboard/add_game.html', context=context)


@login_required
@require_POST
@require_POST_params(['winner', 'loser', 'winner-points', 'loser-points'])
def submit_new_game(request: HttpRequest, league: str) -> HttpResponse:
    '''
    Endpoint for submitting the results of a new game, to be added to the database.
    ''' 
    league_obj = League.objects.get(slug=league)
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
        league=league_obj,
        winner=winner_obj,
        loser=loser_obj,
        winner_points=winner_points,
        loser_points=loser_points
    )
    new_game.save()
    elo_rating.commit_scores(game=new_game)

    return redirect('games')
