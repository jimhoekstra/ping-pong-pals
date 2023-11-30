from django.db import models


class League(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.CharField(max_length=200, unique=True)
    description = models.TextField()

    def __str__(self) -> str:
        return self.name


class Participant(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    player = models.ForeignKey('scoreboard.Player', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.player) + ' in ' + str(self.league)
