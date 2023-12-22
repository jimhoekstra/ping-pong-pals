from typing import Any

from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET, require_POST

from scoreboard.decorators import require_POST_params
from scoreboard.models import League
from scoreboard.state import ApplicationState


@login_required
@require_GET
def page(request: HttpRequest) -> HttpResponse:
    context: dict[str, Any] = {'current_view': 'leagues'}
    all_leagues = League.objects.all()

    context['all_leagues'] = all_leagues
    context['active_user'] = request.user
    context['active_league'] = ApplicationState.get_active_league(request=request)

    return render(request, 'scoreboard/leagues.html', context=context)


@login_required
@require_POST
@require_POST_params(['activate-league-id'])
def activate_league(request: HttpRequest) -> HttpResponse:
    try:
        league = League.objects.get(pk=request.POST['activate-league-id'])
    except League.DoesNotExist:
        return render(request, 'scoreboard/bad_request.html', status=400)

    ApplicationState.set_active_league(request=request, league=league)
    return redirect('leagues')


@login_required
@require_GET
def new_league_page(request: HttpRequest) -> HttpResponse:
    context = {'current_view': 'leagues'}
    return render(request, 'scoreboard/new_league.html', context=context)


@login_required
@require_POST
@require_POST_params(['league-name', 'league-description'])
def submit_new_league(request: HttpRequest) -> HttpResponse:
    new_league = League(
        name=request.POST['league-name'],
        description=request.POST['league-description'],
        owner=request.user.player  # type: ignore
    )
    new_league.save()
    
    return redirect('leagues')
