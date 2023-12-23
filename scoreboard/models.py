from django.db import models
from django.contrib.auth.models import User


class Player(models.Model):
    name = models.CharField(max_length=25, unique=True)
    current_elo = models.IntegerField(default=1000)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name
    

class League(models.Model):
    name = models.CharField(max_length=25, unique=True)
    slug = models.CharField(max_length=50, unique=True)
    description = models.TextField(default='')
    owner = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True)
    participants = models.ManyToManyField(Player, related_name='leagues')

    def __str__(self):
        return self.name
    

class Game(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    league = models.ForeignKey(League, on_delete=models.SET_NULL, null=True, related_name='games')
    winner = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True, related_name='won_games')
    loser = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True, related_name='lost_games')
    winner_points = models.IntegerField()
    loser_points = models.IntegerField()

    def __str__(self):
        if self.winner is None:
            winner_name = '[deleted player]'
        else:
            winner_name = self.winner.name

        if self.loser is None:
            loser_name = '[deleted player]'
        else:
            loser_name = self.loser.name
        
        return (winner_name + ' vs ' + loser_name + ' (' + 
                str(self.winner_points) + '-' + str(self.loser_points) + ')')


class Rating(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField()
    result_of_game = models.ForeignKey(Game, on_delete=models.SET_NULL, null=True)


class CurrentRating(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    rating = models.IntegerField()

    def __str__(self) -> str:
        return 'Current rating of ' + str(self.player) + ' in league' + str(self.league)
