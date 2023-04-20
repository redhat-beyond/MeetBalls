from .models import GameEvent, BallGame
from django.core.exceptions import ValidationError
from court.models import Court
from decimal import Decimal
from datetime import datetime
import pytest

TEST_ID = 2
TEST_TIME = datetime.today()
TEST_LEVEL = 3
TEST_MIN = 2
TEST_MAX = 5
TEST_BALL_GAME = 'Basketball'


@pytest.mark.django_db
class TestGameEventModel:

    @pytest.fixture
    def saved_court(self):
        court = Court.objects.create(x=Decimal('11'), y=Decimal('22'),
                                     city='TEST_CITY', neighborhood='TEST_NEIGHBORHOOD', max_players=30)
        return court

    @pytest.fixture
    def saved_game_event(self, saved_court):
        return GameEvent.objects.create(id=TEST_ID, time=TEST_TIME, level_of_game=TEST_LEVEL,
                                        min_number_of_players=TEST_MIN, max_number_of_players=TEST_MAX,
                                        court_id=saved_court, ball_game=TEST_BALL_GAME)

    def test_get_game_event(self, saved_game_event):
        game_event = GameEvent.objects.get(pk=saved_game_event.pk)
        assert game_event == saved_game_event

    def test_update_game_event(self, saved_game_event):
        game_event = saved_game_event
        assert saved_game_event.ball_game != BallGame.Volleyball
        game_event.ball_game = BallGame.Volleyball
        game_event.save()
        updated_game_event = GameEvent.objects.get(pk=game_event.pk)
        assert updated_game_event.ball_game == BallGame.Volleyball

    def test_delete_game_event(self, saved_game_event):
        pk = saved_game_event.pk
        saved_game_event.delete()
        with pytest.raises(GameEvent.DoesNotExist):
            GameEvent.objects.get(pk=pk)

    def test_create_game_event_with_valid_fields(self, saved_court):
        GameEvent.objects.create(id=TEST_ID, time=TEST_TIME, level_of_game=TEST_LEVEL,
                                 min_number_of_players=TEST_MIN, max_number_of_players=TEST_MAX, court_id=saved_court,
                                 ball_game=TEST_BALL_GAME).full_clean()

    def test_create_game_event_with_invalid_ball_game(self, saved_court):
        with pytest.raises(ValidationError):
            GameEvent.objects.create(id=TEST_ID, time=TEST_TIME, level_of_game=TEST_LEVEL,
                                     min_number_of_players=TEST_MIN, max_number_of_players=TEST_MAX,
                                     court_id=saved_court, ball_game='invalid game').full_clean()

    def test_create_game_event_with_blank_date(self, saved_court):
        with pytest.raises(ValidationError):
            GameEvent.objects.create(id=TEST_ID, time='', level_of_game=TEST_LEVEL,
                                     min_number_of_players=TEST_MIN, max_number_of_players=TEST_MAX,
                                     court_id=saved_court, ball_game=TEST_BALL_GAME).full_clean()

    def test_create_game_event_with_blank_ball_game(self, saved_court):
        with pytest.raises(ValidationError):
            GameEvent.objects.create(id=TEST_ID, time=TEST_TIME, level_of_game=TEST_LEVEL,
                                     min_number_of_players=TEST_MIN, max_number_of_players=TEST_MAX,
                                     court_id=saved_court, ball_game='').full_clean()

    def test_create_game_event_with_null_ball_game(self, saved_court):
        with pytest.raises(ValidationError):
            GameEvent.objects.create(id=TEST_ID, time=TEST_TIME, level_of_game=TEST_LEVEL,
                                     min_number_of_players=TEST_MIN, max_number_of_players=TEST_MAX,
                                     court_id=saved_court,).full_clean()
