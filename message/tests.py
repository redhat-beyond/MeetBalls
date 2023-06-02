from player.models import Player
from game_event.models import GameEvent
from game_event_player.models import GameEventPlayer
from message.models import Message
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.urls import reverse
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
    def saved_message(self, player, game_event):
        message = Message.objects.create(
            user_id=player,
            game_event_id=game_event,
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

    def test_create_message_with_valid_fields(self, player, game_event):
        Message.objects.create(
            user_id=player,
            game_event_id=game_event,
            time_sent=TEST_TIME,
            text="Idan and Ohad").full_clean()

    def test_create_message_with_invalid_text_length(self, player, game_event):
        with pytest.raises(ValidationError):
            Message.objects.create(
                user_id=player,
                game_event_id=game_event,
                time_sent=TEST_TIME,
                text="I" * 260
            ).full_clean()

    def test_create_message_with_empty_text(self, player, game_event):
        with pytest.raises(ValidationError):
            Message.objects.create(
                user_id=player,
                game_event_id=game_event,
                time_sent=TEST_TIME,
                text=""
            ).full_clean()


@pytest.mark.django_db
class TestMessageViews:

    def test_success_send_message(self, client, game_event, player):
        client.force_login(player.user)
        game_event_id = game_event.id
        url = reverse('process_answer_game_event', args=[game_event_id])
        client.post(url, {'answer': 'yes'})
        count_before = Message.objects.count()
        url = reverse('save_text_message', args=[game_event_id])
        response = client.post(url, {'mytextbox': 'Test message'})

        assert response.status_code == 302
        assert Message.objects.count() == count_before + 1
        message = Message.objects.last()
        assert message.user_id == player
        assert message.game_event_id == game_event
        assert message.text == 'Test message'

    def test_messages_persist_after_join_and_remove(self, client, game_event, player):
        client.force_login(player.user)
        game_event_id = game_event.id
        url = reverse('process_answer_game_event', args=[game_event_id])
        response = client.post(url, {'answer': 'yes'}, follow=True)
        assert response.status_code == 200
        url = reverse('save_text_message', args=[game_event_id])
        client.post(url, {'mytextbox': 'hi from user'}, follow=True)
        reverse('remove_from_event', args=[game_event_id])
        player_messages = [entry.text for entry in Message.objects.filter(game_event_id=game_event)]
        assert 'hi from user' in player_messages

    def test_success_create_message_function(self, game_event, player):
        text = 'test message'
        GameEventPlayer.objects.create(game_event=game_event, player=player)
        count_before = Message.objects.count()
        message = Message.create(player, game_event, text)
        assert Message.objects.count() == count_before + 1
        assert message.text == 'test message'

    def test_fail_create_message_function(self, game_event, player):
        text = 'test message'
        count_before = Message.objects.count()
        with pytest.raises(ValidationError):
            Message.create(player, game_event, text)
        assert Message.objects.count() == count_before

    def test_success_validate_message(self, game_event, player):
        GameEventPlayer.objects.create(game_event=game_event, player=player)
        text = 'test message'
        e = Message.validate_message(player, game_event, text)
        assert e is None

    @pytest.mark.parametrize(
        "text, expected_errors",
        [
            ('test message', ["Just players from this event can send messages on chat"]),
            ('', ["Message can't be empty", "Just players from this event can send messages on chat"]),
            ('           ', ["Message can't be empty", "Just players from this event can send messages on chat"]),
        ]
    )
    def test_fail_validate_message(self, game_event, player, text, expected_errors):
        with pytest.raises(ValidationError) as current_errors:
            Message.validate_message(player, game_event, text)
        errors = current_errors.value.messages[0].split("\n")
        assert set(errors) == set(expected_errors)

    def test_failed_send_empty_message(self, client, game_event, player):
        client.force_login(player.user)
        game_event_id = game_event.id
        url = reverse('process_answer_game_event', args=[game_event_id])
        response = client.post(url, {'answer': 'yes'})
        count_before = Message.objects.count()
        url = reverse('save_text_message', args=[game_event_id])
        response = client.post(url, {'mytextbox': ''})
        assert response.status_code == 302
        assert Message.objects.count() == count_before

    def test_failed_send_message_invalid_player(self, client, game_event, player):
        client.force_login(player.user)
        game_event_id = game_event.id
        count_before = Message.objects.count()
        reverse('remove_from_event', args=[game_event_id])
        url = reverse('save_text_message', args=[game_event_id])
        response = client.post(url, {'mytextbox': 'Test message'})

        assert response.status_code == 302
        assert Message.objects.count() == count_before
