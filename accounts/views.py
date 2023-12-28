from typing import Any
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from scoreboard.decorators import require_POST_params
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from accounts.models import SignupKey
from scoreboard.models import Player


@require_GET
def login_page(request: HttpRequest) -> HttpResponse:
    '''
    View of the login page.
    '''

    context_data: dict[str, Any] = {'current_view': 'login'}
    if 'next' in request.GET:
        if request.GET['next'] == '/games':
            context_data['next_page'] = 'games'
        elif request.GET['next'] == '/players':
            context_data['next_page'] = 'players'
        elif request.GET['next'] == '/leagues':
            context_data['next_page'] = 'leagues'
    
    return render(request, 'accounts/login.html', context=context_data)


@require_GET
def new_account_page(request: HttpRequest) -> HttpResponse:
    '''
    View of the new account page.
    '''
    context_data: dict[str, Any] = {'current_view': 'login'}    
    return render(request, 'accounts/new_account.html', context=context_data)


@require_POST
@require_POST_params(['username', 'password'])
def login_user(request: HttpRequest) -> HttpResponse:
    '''
    Endpoint for logging in a user. The username and password submitted on the page
    will be verified, and if valid, the user will be logged in.
    '''
    user = authenticate(request, username=request.POST['username'], password=request.POST['password'])

    if user is None:
        return render(request, 'scoreboard/generic/bad_request.html', status=400)
    
    login(request, user)

    if 'next-page' in request.POST:
        if request.POST['next-page'] == 'games':
            return redirect('games')
        elif request.POST['next-page'] == 'players':
            return redirect('players')

    return redirect('home')


@require_GET
def logout_user(request: HttpRequest) -> HttpResponse:
    '''
    View for logging out a user. Any logged in user will be logged out when
    navigating to this view, and the user will be redirected to the login page.
    '''
    logout(request)
    return redirect('login-page')


@require_POST
@require_POST_params(['username', 'password', 'repeat-password', 'signup-key'])
def create_account(request: HttpRequest) -> HttpResponse:
    '''
    Endpoint for creating a new account, this also logs in the new user if created successfully.
    '''

    try:
        signup_key = SignupKey.objects.get(code=request.POST['signup-key'])
    except SignupKey.DoesNotExist:
        return render(request, 'scoreboard/generic/bad_request.html', status=400)
    
    if request.POST['password'] != request.POST['repeat-password']:
        return render(request, 'scoreboard/generic/bad_request.html', status=400)
    
    new_user = User.objects.create_user(username=request.POST['username'], password=request.POST['password'])
    new_user.save()

    new_player = Player(name=new_user.username, user=new_user)
    new_player.save()    

    signup_key.used = True
    signup_key.used_by = new_user
    signup_key.save()

    login(request, new_user)

    return redirect('home')


@login_required
@require_GET
def overview(request: HttpRequest) -> HttpResponse:
    user_obj = request.user
    player_obj = Player.objects.get(user=user_obj)

    context_dict = {
        'player_name': player_obj.name,
        'current_view': 'account'
    }

    return render(request, 'accounts/overview.html', context=context_dict)


@login_required
@require_POST
@require_POST_params(['new-profile-name'])
def update_profile_name(request: HttpRequest) -> HttpResponse:
    user_obj = request.user
    player_obj = Player.objects.get(user=user_obj)

    player_obj.name = request.POST['new-profile-name']
    player_obj.save()

    return redirect('account-overview')


@login_required
@require_POST
@require_POST_params(['old-password', 'new-password', 'repeat-new-password'])
def update_password(request: HttpRequest) -> HttpResponse:
    username: str = request.user.username  # type: ignore

    if request.POST['new-password'] != request.POST['repeat-new-password']:
        return render(request, 'scoreboard/bad_request.html', status=400)
    
    authenticated_user = authenticate(username=username, password=request.POST['old-password'])
    if authenticated_user is None:
        return render(request, 'scoreboard/bad_request.html', status=400)
    
    logout(request)
    authenticated_user.set_password(request.POST['new-password'])
    authenticated_user.save()
    
    return redirect('account-overview')
