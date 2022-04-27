from django.shortcuts import render, redirect
from django.views import View
from .models import Game, Player
from .forms import NewGameForm, NewPlayerForm
from .elo import EloRating


def index(request):
    return redirect('games')


class GamesView(View):

    def get_context_data(self, **kwargs):
        context = {}
        context['current_view'] = 'games'
        context['new_game_form'] = NewGameForm()
        context['all_games'] = Game.objects.all().order_by('-date')
        return context

    def get(self, request):
        context = self.get_context_data()
        return render(request, 'elo/games.html', context=context)

    def post(self, request):
        form = NewGameForm(request.POST)
        if form.is_valid():
            winner = Player.objects.get(pk=form.cleaned_data['winner'])
            loser = Player.objects.get(pk=form.cleaned_data['loser'])
            elo_rating = EloRating(winner, loser)

            new_game = Game(
                winner=winner,
                loser=loser,
                winner_elo_before=winner.current_elo,
                winner_elo_after=elo_rating.get_new_winner_rating(),
                loser_elo_before=loser.current_elo,
                loser_elo_after=elo_rating.get_new_loser_rating()
            )
            new_game.save()
            elo_rating.commit_scores()

        return redirect('games')


class PlayersView(View):

    def get_context_data(self, **kwargs):
        context = {}
        context['current_view'] = 'players'
        context['new_player_form'] = NewPlayerForm()
        context['all_players'] = Player.objects.all().order_by('-current_elo')
        return context

    def get(self, request):
        context = self.get_context_data()
        return render(request, 'elo/players.html', context=context)

    def post(self, request):
        form = NewPlayerForm(request.POST)
        if form.is_valid():
            new_player = Player(name=form.cleaned_data['name'])
            new_player.save()
        
        return redirect('players')
