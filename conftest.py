from player.models import BallGame, Player
from court.models import Court
from court_ball_game.models import CourtBallGame
from decimal import Decimal
import pytest


@pytest.fixture
def player():
    player = Player.create(
        username='Player',
        password='password',
        birth_date='1990-01-01',
        favorite_ball_game=BallGame.Soccer)
    return player


@pytest.fixture
def court():
    court = Court.objects.create(x=Decimal('11'), y=Decimal('22'),
                                 city='TEST_CITY', neighborhood='TEST_NEIGHBORHOOD', max_players=30)
    return court


@pytest.fixture
def court_ball_game(court):
    court_ball_game = CourtBallGame.objects.create(court=court, ball_game=BallGame.Basketball)
    return court_ball_game
