from player.models import BallGame, Player
from django.contrib.auth import get_user_model
import pytest


@pytest.fixture
def user():
    return get_user_model().objects.create_user(
        username='testuser',
        password='testpass')


@pytest.fixture
def player(user):
    player = Player.objects.create(
        user=user,
        birth_date='1990-01-01',
        favorite_ball_game=BallGame.Soccer)
    return player
