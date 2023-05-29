from django.contrib.auth import get_user_model
from player.models import Player, BallGame
from game_event.models import GameEvent
from message.models import Message
from django.core.exceptions import ValidationError
from django.utils import timezone
import pytest

TEST_ID = 2
TEST_TIME = timezone.now()
TEST_LEVEL = 3
TEST_MIN = 2
TEST_MAX = 5
TEST_BALL_GAME = 'Basketball'


@pytest.mark.django_db
class TestMessageModel:

    @pytest.fixture
    def user(self):
        return get_user_model().objects.create_user(
            username='testuser',
            password='testpass'
        )

    @pytest.fixture
    def saved_player(self, user):
        player = Player.objects.create(
            user=user,
            birth_date='1990-01-01',
            favorite_ball_game=BallGame.Soccer
        )
        return player

    @pytest.fixture
    def saved_game_event(self, court):
        return GameEvent.objects.create(id=TEST_ID, time=TEST_TIME, level_of_game=TEST_LEVEL,
                                        min_number_of_players=TEST_MIN, max_number_of_players=TEST_MAX,
                                        court=court, ball_game=TEST_BALL_GAME)

    @pytest.fixture
    def saved_message(self, saved_player, saved_game_event):
        message = Message.objects.create(
            user_id=saved_player,
            game_event_id=saved_game_event,
            time_sent=TEST_TIME,
            text="test message"
        )
        return message

    def test_get_message(self, saved_message):
        message = Message.objects.get(pk=saved_message.pk)
        assert message == saved_message

    def test_update_message(self, saved_message):
        new_text = "test message?!"
        message = saved_message
        assert message.text != new_text
        message.text = new_text
        message.save()
        updated_message = Message.objects.get(pk=message.pk)
        assert updated_message.text == new_text

    def test_delete_message(self, saved_message):
        message = saved_message
        message.delete()
        with pytest.raises(Message.DoesNotExist):
            Message.objects.get(pk=saved_message.pk)

    def test_delete_game_event_deletes_message(self, saved_message):
        game_event = GameEvent.objects.get(id=saved_message.game_event_id.id)
        game_event.delete()
        with pytest.raises(Message.DoesNotExist):
            Message.objects.get(pk=saved_message.pk)

    def test_delete_user_deletes_message(self, saved_message):
        player = Player.objects.get(user=saved_message.user_id)
        player.delete()
        with pytest.raises(Message.DoesNotExist):
            Message.objects.get(pk=saved_message.pk)

    def test_create_message_with_valid_fields(self, saved_player, saved_game_event):
        Message.objects.create(
            user_id=saved_player,
            game_event_id=saved_game_event,
            time_sent=TEST_TIME,
            text="Idan and Ohad").full_clean()

    def test_create_message_with_invalid_text_length(self, saved_player, saved_game_event):
        with pytest.raises(ValidationError):
            Message.objects.create(
                user_id=saved_player,
                game_event_id=saved_game_event,
                time_sent=TEST_TIME,
                text="I" * 260
            ).full_clean()

    def test_create_message_with_empty_text(self, saved_player, saved_game_event):
        with pytest.raises(ValidationError):
            Message.objects.create(
                user_id=saved_player,
                game_event_id=saved_game_event,
                time_sent=TEST_TIME,
                text=""
            ).full_clean()
