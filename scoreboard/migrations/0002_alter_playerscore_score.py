# Generated by Django 4.1.5 on 2023-10-28 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scoreboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playerscore',
            name='score',
            field=models.IntegerField(),
        ),
    ]
