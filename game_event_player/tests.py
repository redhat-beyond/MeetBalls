from django.contrib.auth import get_user_model
import pytest
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from .models import GameEventPlayer
from game_event.models import GameEvent
from player.models import Player, BallGame
from court.models import Court
from decimal import Decimal
from datetime import datetime


ID1 = 2
ID2 = 3


@pytest.fixture
def user():
    return get_user_model().objects.create_user(
        username='testuser',
        password='testpass'
    )


@pytest.fixture
def user2():
    return get_user_model().objects.create_user(
        username='testuser2',
        password='testpass'
    )


@pytest.fixture
def user3():
    return get_user_model().objects.create_user(
        username='testuser3',
        password='testpass'
    )


@pytest.fixture
def saved_player(user):
    player = Player.objects.create(
        user=user,
        birth_date='1990-01-01',
        favorite_ball_game=BallGame.Soccer
    )
    return player


@pytest.fixture
def saved_player2(user2):
    player = Player.objects.create(
        user=user2,
        birth_date='1990-01-01',
        favorite_ball_game=BallGame.Soccer
    )
    return player


@pytest.fixture
def saved_player3(user3):
    player = Player.objects.create(
        user=user3,
        birth_date='1990-01-01',
        favorite_ball_game=BallGame.Soccer
    )
    return player


@pytest.fixture
def players(saved_player, saved_player2, saved_player3):
    return tuple([saved_player, saved_player2, saved_player3])


@pytest.fixture
def saved_court():
    court = Court.objects.create(x=Decimal('11'), y=Decimal('22'),
                                 city='TEST_CITY', neighborhood='TEST_NEIGHBORHOOD', max_players=30)
    return court


@pytest.fixture
def saved_game_event(saved_court):
    game_event = GameEvent.objects.create(id=ID1, time=datetime.today(), level_of_game=3,
                                          min_number_of_players=2, max_number_of_players=5, court=saved_court,
                                          ball_game='Basketball')
    return game_event


@pytest.fixture
def saved_game_event2(saved_court):
    game_event = GameEvent.objects.create(id=ID2, time=datetime.today(), level_of_game=3,
                                          min_number_of_players=2, max_number_of_players=5, court=saved_court,
                                          ball_game='Basketball')
    return game_event


@pytest.fixture
def saved_game_event_player(saved_game_event, saved_player):
    return GameEventPlayer.objects.create(game_event_id=saved_game_event, player_id=saved_player,
                                          ball_responsible=False)


@pytest.mark.django_db
class TestGameEventPlayerModel:

    def test_game_event_player_creation(self, saved_game_event, saved_player):
        game_event_player = GameEventPlayer.objects.create(game_event_id=saved_game_event, player_id=saved_player,)
        game_event_player.full_clean()
        assert game_event_player.game_event_id == saved_game_event
        assert game_event_player.player_id == saved_player
        assert game_event_player.ball_responsible is False

    def test_filter_players_by_event(self, saved_game_event, saved_game_event2, players):
        GameEventPlayer.objects.create(game_event_id=saved_game_event, player_id=players[0], ball_responsible=False)
        GameEventPlayer.objects.create(game_event_id=saved_game_event, player_id=players[1], ball_responsible=False)
        GameEventPlayer.objects.create(game_event_id=saved_game_event, player_id=players[2], ball_responsible=False)
        GameEventPlayer.objects.create(game_event_id=saved_game_event2, player_id=players[0], ball_responsible=False)
        GameEventPlayer.objects.create(game_event_id=saved_game_event2, player_id=players[1], ball_responsible=False)
        p1 = GameEventPlayer.objects.filter(player_id=players[0])
        events = sorted([entry.game_event_id.id for entry in p1])
        expected_events = sorted([ID1, ID2])
        assert expected_events == events
        e1 = GameEventPlayer.objects.filter(game_event_id=saved_game_event)
        players = sorted([entry.player_id.user for entry in e1], key=str)
        expected_players = sorted(players, key=str)
        assert expected_players == players

    def test_unique_together_constraint(self, saved_game_event, saved_player):
        GameEventPlayer.objects.create(game_event_id=saved_game_event, player_id=saved_player, ball_responsible=False)
        with pytest.raises(IntegrityError):
            GameEventPlayer.objects.create(game_event_id=saved_game_event, player_id=saved_player,
                                           ball_responsible=False)

    def test_get_game_event_player(self, saved_game_event_player):
        game_event_player = GameEventPlayer.objects.get(pk=saved_game_event_player.pk)
        assert game_event_player == saved_game_event_player

    def test_create_game_event_player_with_empty_player(self, saved_game_event):
        with pytest.raises(IntegrityError):
            GameEventPlayer.objects.create(game_event_id=saved_game_event, player_id=Player.objects.create(),
                                           ball_responsible=False)

    def test_create_game_event_player_with_empty_game_event(self, saved_player):
        with pytest.raises(IntegrityError):
            GameEventPlayer.objects.create(game_event_id=GameEvent.objects.create(), player_id=saved_player,
                                           ball_responsible=False)

    def test_create_game_event_player_with_blank_ball_responsible(self, saved_game_event, saved_player):
        with pytest.raises(ValidationError):
            GameEventPlayer.objects.create(game_event_id=saved_game_event, player_id=saved_player,
                                           ball_responsible='').full_clean()

    def test_create_game_event_player_with_invalid_ball_responsible(self, saved_game_event, saved_player):
        with pytest.raises(ValidationError):
            GameEventPlayer.objects.create(game_event_id=saved_game_event, player_id=saved_player,
                                           ball_responsible='invalid - should be boolean').full_clean()
