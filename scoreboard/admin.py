from django.contrib import admin
from .models import Game, Player, Rating, League, CurrentRating


admin.site.register(Game)
admin.site.register(Player)
admin.site.register(Rating)
admin.site.register(League)
admin.site.register(CurrentRating)
