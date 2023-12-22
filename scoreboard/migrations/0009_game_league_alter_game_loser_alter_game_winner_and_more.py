# Generated by Django 4.1.5 on 2023-12-22 19:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scoreboard', '0008_league_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='league',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='games', to='scoreboard.league'),
        ),
        migrations.AlterField(
            model_name='game',
            name='loser',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lost_games', to='scoreboard.player'),
        ),
        migrations.AlterField(
            model_name='game',
            name='winner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='won_games', to='scoreboard.player'),
        ),
        migrations.AlterField(
            model_name='league',
            name='name',
            field=models.CharField(max_length=25, unique=True),
        ),
        migrations.AlterField(
            model_name='league',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='scoreboard.player'),
        ),
        migrations.AlterField(
            model_name='player',
            name='name',
            field=models.CharField(max_length=25, unique=True),
        ),
        migrations.AlterField(
            model_name='rating',
            name='result_of_game',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='scoreboard.game'),
        ),
    ]