from player.models import BallGame, Player
from court.models import Court
from court_ball_game.models import CourtBallGame
from notification.models import Notification, NotificationType
from django.utils import timezone
from decimal import Decimal
from player_rating.models import PlayerRating
from game_event.models import GameEvent
from game_event_player.models import GameEventPlayer
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
def player_rating(player):
    return PlayerRating.objects.create(ball_game=BallGame.Baseball, player=player, rating=5)


@pytest.fixture
def court():
    court = Court.objects.create(x=Decimal('11'), y=Decimal('22'),
                                 city='TEST_CITY', neighborhood='TEST_NEIGHBORHOOD', max_players=30)
    return court


@pytest.fixture
def court_ball_game(court):
    court_ball_game = CourtBallGame.objects.create(court=court, ball_game=BallGame.Basketball)
    return court_ball_game


@pytest.fixture
def notification(player):
    return Notification.objects.create(
        player=player,
        sent_time=timezone.now(),
        message='Test notification',
        notification_type=NotificationType.WEBSITE,
        is_read=False
    )


@pytest.fixture
def game_event(court):
    return GameEvent.objects.create(
        id=2,
        time=timezone.now(),
        level_of_game=3,
        min_number_of_players=2,
        max_number_of_players=5,
        court=court,
        ball_game=BallGame.Baseball
        )


@pytest.fixture
def game_event_player(game_event, player):
    return GameEventPlayer.objects.create(
        game_event=game_event,
        player=player,
        ball_responsible=False
        )
