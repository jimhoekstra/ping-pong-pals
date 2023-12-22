from django.contrib import admin
from .models import Game, Player, Rating, League


admin.site.register(Game)
admin.site.register(Player)
admin.site.register(Rating)
admin.site.register(League)
