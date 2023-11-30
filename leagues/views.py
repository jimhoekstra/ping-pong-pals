from typing import Any
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from scoreboard.decorators import require_POST_params
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from leagues.models import League


@login_required
@require_GET
def overview(request: HttpRequest) -> HttpResponse:
    context: dict[str, Any] = {'current_view': 'leagues'}

    all_leagues = League.objects.all()
    print(all_leagues)
    context['all_leagues'] = all_leagues

    return render(request, 'leagues/overview.html', context=context)


@login_required
@require_GET
def new_league_page(request: HttpRequest) -> HttpResponse:
    context: dict[str, Any] = {'current_view': 'leagues'}
    return render(request, 'leagues/new.html', context=context)


@login_required
@require_POST
@require_POST_params(['league-name'])
def create_new_league(request: HttpRequest) -> HttpResponse:
    new_league = League(name=request.POST['league-name'])
    new_league.save()

    return redirect('leagues-overview')


@login_required
@require_POST
def submit_join_request(request: HttpRequest) -> HttpResponse:
    return redirect('leagues-overview')


@login_required
@require_POST
def activate_league(request: HttpRequest) -> HttpResponse:
    return redirect('leagues-overview')
