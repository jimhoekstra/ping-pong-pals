from django.db import models
from django.contrib.auth.models import User


class Player(models.Model):
    name = models.CharField(max_length=25)
    current_elo = models.IntegerField(default=800)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Game(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    winner: models.ForeignKey[Player] = models.ForeignKey(
        'Player', on_delete=models.CASCADE, related_name='won_games')
    loser: models.ForeignKey[Player] = models.ForeignKey(
        'Player', on_delete=models.CASCADE, related_name='lost_games')
    winner_points = models.IntegerField()
    loser_points = models.IntegerField()
    winner_elo_before = models.FloatField()
    winner_elo_after = models.FloatField()
    loser_elo_before = models.FloatField()
    loser_elo_after = models.FloatField()
