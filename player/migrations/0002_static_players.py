from django.db import migrations
from django.db import transaction
from django.db import models
import datetime
import random


class BallGame(models.TextChoices):
    Soccer = 'Soccer', 'Soccer'
    Basketball = 'Basketball', 'Basketball'
    Volleyball = 'Volleyball', 'Volleyball'
    Baseball = 'Baseball', 'Baseball'
    Tennis = 'Tennis', 'Tennis'
    Rugby = 'Rugby', 'Rugby'
    Golf = 'Golf', 'Golf'
    Cricket = 'Cricket', 'Cricket'
    Handball = 'Handball', 'Handball'


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0001_initial'),
    ]

    def generate_data(apps, schema_editor):

        from player.models import Player
        password = 'password123'
        static_players = []
        for i in range(5):
            username = f'user{i + 1}'
            random_birth_date = datetime.date(1950, 1, 1) + datetime.timedelta(days=random.randint(0, 20055))
            random_favorite_ball_game = random.choice(BallGame.choices)[0]
            static_players.append((username, password, random_birth_date, random_favorite_ball_game))

        with transaction.atomic():
            for username, password, birth_date, favorite_ball_game in static_players:
                Player.create(username=username, password=password, birth_date=birth_date,
                              favorite_ball_game=favorite_ball_game)

    operations = [
            migrations.RunPython(generate_data),
        ]
