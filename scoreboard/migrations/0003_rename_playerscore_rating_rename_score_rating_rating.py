# Generated by Django 4.1.5 on 2023-12-22 14:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scoreboard', '0002_alter_playerscore_score'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PlayerScore',
            new_name='Rating',
        ),
        migrations.RenameField(
            model_name='rating',
            old_name='score',
            new_name='rating',
        ),
    ]
