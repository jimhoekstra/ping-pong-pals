from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from elo.decorators import require_POST_params
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth import authenticate, login, logout


@require_GET
def login_page(request: HttpRequest) -> HttpResponse:
    return render(request, 'accounts/login.html')


@require_POST
@require_POST_params(['username', 'password'])
def login_user(request: HttpRequest) -> HttpResponse:
    user = authenticate(request, username=request.POST['username'], password=request.POST['password'])

    if user is None:
        return render(request, 'elo/bad_request.html', status=400)
    
    login(request, user)
    return redirect('games')


@require_GET
def logout_user(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect('login-page')
