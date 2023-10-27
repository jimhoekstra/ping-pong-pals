from django import forms
from .models import Player


class NewPlayerForm(forms.Form):
    name = forms.CharField(label='Name', max_length=25, 
                widget=forms.TextInput(attrs={
                    'class': 'form-control',
                    'placeholder': 'Name...'
                }))


def get_all_players() -> list[tuple[int, str]]:
    return [
            (player.pk, player.name) for player in Player.objects.all()
        ]


class NewGameForm(forms.Form):

    winner = forms.ChoiceField(choices=get_all_players, widget=forms.Select(attrs={
                    'class': 'form-select'
                }))
    loser = forms.ChoiceField(choices=get_all_players, widget=forms.Select(attrs={
                    'class': 'form-select'
                }))
