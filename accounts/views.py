from typing import Any
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from scoreboard.decorators import require_POST_params
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth import authenticate, login, logout
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
    
    return render(request, 'accounts/login.html', context=context_data)


@require_POST
@require_POST_params(['username', 'password'])
def login_user(request: HttpRequest) -> HttpResponse:
    '''
    Endpoint for logging in a user. The username and password submitted on the page
    will be verified, and if valid, the user will be logged in.
    '''
    user = authenticate(request, username=request.POST['username'], password=request.POST['password'])

    if user is None:
        return render(request, 'scoreboard/bad_request.html', status=400)
    
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
        return render(request, 'scoreboard/bad_request.html', status=400)
    
    if request.POST['password'] != request.POST['repeat-password']:
        return render(request, 'scoreboard/bad_request.html', status=400)
    
    new_user = User.objects.create_user(username=request.POST['username'], password=request.POST['password'])
    new_user.save()

    new_player = Player(name=new_user.username, user=new_user)
    new_player.save()    

    signup_key.used = True
    signup_key.used_by = new_user
    signup_key.save()

    login(request, new_user)

    return redirect('home')
