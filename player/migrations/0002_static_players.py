from django.db import migrations, transaction, models
from player.models import BallGame
import datetime
import random


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
            static_players.append((username, random_birth_date, random_favorite_ball_game))

        with transaction.atomic():
            for username, birth_date, favorite_ball_game in static_players:
                Player.create(username=username, password=password, birth_date=birth_date,
                              favorite_ball_game=favorite_ball_game)

    operations = [
        migrations.AddField(
            model_name='player',
            name='profile_pic',
            field=models.ImageField(default='default-profile-pic.png', upload_to='profile_pictures'),
        ), migrations.RunPython(generate_data),
        ]
