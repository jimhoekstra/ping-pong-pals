from datetime import datetime

from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET, require_POST
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone

from accounts.models import SignupKey

from scoreboard.decorators import require_POST_params, verify_access_to_league
from scoreboard.models import League, Player
from scoreboard.state import ApplicationState
from scoreboard.views.leagues.context import LeagueContext


@login_required
@require_GET
def page(request: HttpRequest) -> HttpResponse:
    context = (LeagueContext(request=request)
                .set_page_title('Your Leagues')
                .set_next_page_url_name('league-detail')
                .add_current_league_from_app_state_if_exists()
                .add_logged_in_player()
                .add_all_leagues_info()
                .as_context_dict())

    return render(request, 'scoreboard/leagues/page.html', context=context)


@login_required
@verify_access_to_league
@require_GET
def detail_page(request: HttpRequest, league: str) -> HttpResponse:
    try:
        league_obj = League.objects.get(slug=league)
    except League.DoesNotExist:
        return render(request, 'scoreboard/bad_request.html', status=400)
     
    context = (LeagueContext(request=request)
               .as_context_dict())
    
    player: Player = request.user.player  # type: ignore
    is_owner = league_obj.owner == player
    now = timezone.now()

    context['league'] = league_obj
    context['is_owner'] = is_owner
    context['n_participants'] = league_obj.participants.count()
    context['n_games'] = league_obj.games.count()  # type: ignore
    context['n_games_this_month'] = league_obj.games.filter(  # type: ignore
        date__gte=datetime(year=now.year, month=now.month, day=1)).count()

    if is_owner:
        context['url_prefix'] = reverse('new-account-page')
        existing_sign_up_tokens = SignupKey.objects.filter(
            add_as_member_of=league_obj,
            used=False
        )
        context['existing_sign_up_tokens'] = existing_sign_up_tokens
        context['n_sign_up_tokens'] = len(existing_sign_up_tokens)

    return render(request, 'scoreboard/leagues/detail.html', context=context)


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
    return redirect('not-implemented')

    # new_league = League(
    #     name=request.POST['league-name'],
    #     slug=slugify(request.POST['league-name']),
    #     description=request.POST['league-description'],
    #     owner=request.user.player  # type: ignore
    # )
    # new_league.save()

    # new_league.participants.add(request.user.player)  # type: ignore
    
    # return redirect('leagues')
