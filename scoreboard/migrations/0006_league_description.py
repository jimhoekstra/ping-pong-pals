# Generated by Django 4.1.5 on 2023-12-22 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scoreboard', '0005_league'),
    ]

    operations = [
        migrations.AddField(
            model_name='league',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]