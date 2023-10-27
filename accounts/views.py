from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from scoreboard.decorators import require_POST_params
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth import authenticate, login, logout


@require_GET
def login_page(request: HttpRequest) -> HttpResponse:
    '''
    View of the login page.
    '''
    return render(request, 'accounts/login.html')


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
    return redirect('players')


@require_GET
def logout_user(request: HttpRequest) -> HttpResponse:
    '''
    View for logging out a user. Any logged in user will be logged out when
    navigating to this view, and the user will be redirected to the login page.
    '''
    logout(request)
    return redirect('login-page')
