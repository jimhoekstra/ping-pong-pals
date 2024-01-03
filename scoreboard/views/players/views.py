from typing import Any

from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET

from scoreboard.models import Player, League
from scoreboard.state import ApplicationState
from scoreboard.views.leagues.context import LeagueContext
from scoreboard.views.players.context import PlayersContext


@login_required
@require_GET
def select_league_page(request: HttpRequest) -> HttpResponse:
    active_league = ApplicationState.get_active_league(request=request)
    if active_league is not None:
        return redirect('players-for-league', league=active_league.slug)
    
    context = (LeagueContext(request=request)
                .override_current_view('players')
                .set_page_title('Players')
                .set_next_page_url_name('players-for-league')
                .add_current_league_from_app_state_if_exists()
                .add_logged_in_player()
                .add_all_leagues_info()
                .as_context_dict())

    return render(request, 'scoreboard/leagues/page.html', context=context)


@login_required
@require_GET
def page(request: HttpRequest, league: str) -> HttpResponse:
    '''
    View of all the players, ordered by descending Elo rating, also showing
    the number of games that a player has logged.
    '''
    league_obj = League.objects.get(slug=league)

    context: dict[str, Any] = (PlayersContext(request=request)
                               .add_current_league(league=league_obj)
                               .add_all_players()
                               .as_context_dict())
    
    return render(request, 'scoreboard/players/page.html', context=context)


@login_required
@require_GET
def single_player_without_page(request: HttpRequest, league: str, player_name: str) -> HttpResponse:
    return redirect('player', league=league, player_name=player_name, page=1)


@login_required
@require_GET
def single_player_page(request: HttpRequest, league: str, player_name: str, page: int) -> HttpResponse:
    '''
    See a player's game and score history.
    '''
    league_obj = League.objects.get(slug=league)

    GAMES_PER_PAGE: int = 10

    try:
        player_obj = Player.objects.get(name=player_name)
    except Player.DoesNotExist:
        return render(request, 'scoreboard/bad_request.html', status=400)
    
    context: dict[str, Any] = (PlayersContext(request=request)
                               .add_current_league(league=league_obj)
                               .add_single_player_info(player=player_obj, page=page, games_per_page=GAMES_PER_PAGE)
                               .as_context_dict())
    
    return render(request, 'scoreboard/players/player.html', context=context)


@login_required
@require_GET
def games_for_player(request: HttpRequest, league: str, player_name: str, page: int = 1) -> HttpResponse:
    '''
    See a player's recent games.
    '''
    league_obj = League.objects.get(slug=league)

    GAMES_PER_PAGE: int = 10

    try:
        player_obj = Player.objects.get(name=player_name)
    except Player.DoesNotExist:
        return render(request, 'scoreboard/bad_request.html', status=400)
    
    context: dict[str, Any] = (PlayersContext(request=request)
                               .add_current_league(league=league_obj)
                               .add_single_player_info(player=player_obj, page=page, games_per_page=GAMES_PER_PAGE)
                               .as_context_dict())
    
    return render(request, 'scoreboard/players/games_for_player.html', context=context)
