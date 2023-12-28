from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET, require_POST
from django.utils.text import slugify

from scoreboard.decorators import require_POST_params
from scoreboard.models import League
from scoreboard.state import ApplicationState
from scoreboard.views.leagues.context import LeagueContext


@login_required
@require_GET
def page(request: HttpRequest) -> HttpResponse:
    context = (LeagueContext(request=request)
                .set_page_title('Leagues')
                .set_next_page_url_name('league-detail')
                .add_current_league_from_app_state_if_exists()
                .add_logged_in_player()
                .add_all_leagues_info()
                .as_context_dict())

    return render(request, 'scoreboard/leagues/page.html', context=context)


@login_required
@require_GET
def detail_page(request: HttpRequest, league: str) -> HttpResponse:
    return redirect('leagues')


@login_required
@require_POST
@require_POST_params(['activate-league-id', 'next-page-name'])
def activate_league(request: HttpRequest) -> HttpResponse:
    try:
        league = League.objects.get(pk=request.POST['activate-league-id'])
    except League.DoesNotExist:
        return render(request, 'scoreboard/bad_request.html', status=400)

    ApplicationState.set_active_league(request=request, league=league)
    
    if request.POST['next-page-name'] == 'games':
        return redirect('games')
    if request.POST['next-page-name'] == 'players':
        return redirect('players')
    if request.POST['next-page-name'] == 'leagues':
        return redirect('leagues')
    
    return redirect('home')


@login_required
@require_POST
@require_POST_params(['next-page-name'])
def deactivate_league(request: HttpRequest) -> HttpResponse:
    ApplicationState.remove_active_league(request=request)

    if request.POST['next-page-name'] == 'games':
        return redirect('games')
    if request.POST['next-page-name'] == 'players':
        return redirect('players')
    if request.POST['next-page-name'] == 'leagues':
        return redirect('leagues')
    
    return redirect('home')


@login_required
@require_GET
def new_league_page(request: HttpRequest) -> HttpResponse:
    context = LeagueContext(request=request).as_context_dict()
    return render(request, 'scoreboard/leagues/new_league.html', context=context)


@login_required
@require_POST
@require_POST_params(['league-name', 'league-description'])
def submit_new_league(request: HttpRequest) -> HttpResponse:
    new_league = League(
        name=request.POST['league-name'],
        slug=slugify(request.POST['league-name']),
        description=request.POST['league-description'],
        owner=request.user.player  # type: ignore
    )
    new_league.save()

    new_league.participants.add(request.user.player)  # type: ignore
    
    return redirect('leagues')
