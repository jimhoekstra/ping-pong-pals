from django.shortcuts import render, redirect


def index(request):
    return redirect('games')


def games(request):
    context = {'current_view': 'games'}
    return render(request, 'elo/games.html', context=context)


def players(request):
    context = {'current_view': 'players'}
    return render(request, 'elo/players.html', context=context)
