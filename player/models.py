from django.contrib.auth.models import User
from django.db import models


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


class Player(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True)
    birth_date = models.DateField()
    favorite_ball_game = models.CharField(
        max_length=100,
        choices=BallGame.choices)

    @staticmethod
    def create(username, password, birth_date, favorite_ball_game):
        player = Player(user=User.objects.create_user(
                    username=username,
                    password=password), birth_date=birth_date, favorite_ball_game=favorite_ball_game)
        player.user.save()
        player.save()
        return player
