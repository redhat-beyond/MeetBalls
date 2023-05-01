from player.models import BallGame, Player
import pytest


@pytest.fixture
def player():
    player = Player.create(
        username='daniel',
        password='password',
        birth_date='1990-01-01',
        favorite_ball_game=BallGame.Soccer)
    return player
