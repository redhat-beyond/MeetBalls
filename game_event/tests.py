from .models import GameEvent
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from player.models import BallGame
from django.urls import reverse
from .views import process_game_event_form
from game_event_player.models import GameEventPlayer
from datetime import timedelta
import pytest
from django.db import IntegrityError

TEST_ID = 2
TEST_TIME = timezone.now()
TEST_LEVEL = 3
TEST_MIN = 2
TEST_MAX = 5
TEST_BALL_GAME = 'Basketball'


@pytest.fixture
def saved_game_event(court):
    return GameEvent.objects.create(id=TEST_ID, time=TEST_TIME, level_of_game=TEST_LEVEL,
                                    min_number_of_players=TEST_MIN, max_number_of_players=TEST_MAX,
                                    court=court, ball_game=TEST_BALL_GAME)


@pytest.fixture
def saved_game_event_player(saved_game_event, player):
    return GameEventPlayer.objects.create(game_event=saved_game_event, player=player,
                                          ball_responsible=False)


@pytest.mark.django_db
class TestGameEventModel:

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

    def test_create_game_event_with_valid_fields(self, court):
        GameEvent.objects.create(id=TEST_ID, time=TEST_TIME, level_of_game=TEST_LEVEL,
                                 min_number_of_players=TEST_MIN, max_number_of_players=TEST_MAX, court=court,
                                 ball_game=TEST_BALL_GAME).full_clean()

    def test_create_game_event_with_invalid_ball_game(self, court):
        with pytest.raises(ValidationError):
            GameEvent.objects.create(id=TEST_ID, time=TEST_TIME, level_of_game=TEST_LEVEL,
                                     min_number_of_players=TEST_MIN, max_number_of_players=TEST_MAX,
                                     court=court, ball_game='invalid game').full_clean()

    def test_create_game_event_with_blank_date(self, court):
        with pytest.raises(ValidationError):
            GameEvent.objects.create(id=TEST_ID, time='', level_of_game=TEST_LEVEL,
                                     min_number_of_players=TEST_MIN, max_number_of_players=TEST_MAX,
                                     court=court, ball_game=TEST_BALL_GAME).full_clean()

    def test_create_game_event_with_blank_ball_game(self, court):
        with pytest.raises(ValidationError):
            GameEvent.objects.create(id=TEST_ID, time=TEST_TIME, level_of_game=TEST_LEVEL,
                                     min_number_of_players=TEST_MIN, max_number_of_players=TEST_MAX,
                                     court=court, ball_game='').full_clean()

    def test_create_game_event_with_null_ball_game(self, court):
        with pytest.raises(ValidationError):
            GameEvent.objects.create(id=TEST_ID, time=TEST_TIME, level_of_game=TEST_LEVEL,
                                     min_number_of_players=TEST_MIN, max_number_of_players=TEST_MAX,
                                     court=court,).full_clean()

    def test_create_game_event_valid_form(self, client, court, court_ball_game):
        count_of_game_events_before = GameEvent.objects.count()
        url = reverse(process_game_event_form)
        time_now_plus_one_day = (timezone.now() + timedelta(days=1)).strftime('%Y-%m-%dT%H:%M')
        form_data = {
            'time': time_now_plus_one_day,
            'level_of_game': 5,
            'min_number_of_players': 2,
            'max_number_of_players': 4,
            'court': court.courtID,
            'ball_game': TEST_BALL_GAME,
        }
        client.post(url, data=form_data)
        assert GameEvent.objects.count() == count_of_game_events_before + 1

    def test_validate_game_event_creation_bad_time(self, court, court_ball_game):
        bad_test_time = timezone.datetime.fromisoformat("2022-05-10T14:30")
        bad_test_time = timezone.make_aware(bad_test_time)
        with pytest.raises(ValidationError):
            GameEvent.validate_game_event(
                court=court.courtID,
                ball_game=TEST_BALL_GAME,
                min_number_of_players=2,
                max_number_of_players=4,
                time=bad_test_time)

    def test_validate_game_event_creation_bad_ball_game(self, court, court_ball_game):
        time_now_plus_one_day = timezone.now() + timedelta(days=1)
        with pytest.raises(ValidationError):
            GameEvent.validate_game_event(
                court=court.courtID,
                ball_game="Golf",
                min_number_of_players=2,
                max_number_of_players=4,
                time=time_now_plus_one_day)

    def test_validate_game_event_creation_negative_min_players(self, court, court_ball_game):
        time_now_plus_one_day = timezone.now() + timedelta(days=1)
        with pytest.raises(ValidationError):
            GameEvent.validate_game_event(
                court=court.courtID,
                ball_game=TEST_BALL_GAME,
                min_number_of_players=-1,
                max_number_of_players=4,
                time=time_now_plus_one_day)

    def test_validate_game_event_creation_max_players_less_then_min_players(self, court, court_ball_game):
        time_now_plus_one_day = timezone.now() + timedelta(days=1)
        with pytest.raises(ValidationError):
            GameEvent.validate_game_event(
                court=court.courtID,
                ball_game=TEST_BALL_GAME,
                min_number_of_players=2,
                max_number_of_players=1,
                time=time_now_plus_one_day)

    def test_validate_game_event_creation(self, court, court_ball_game):
        time_now_plus_one_day = timezone.now() + timedelta(days=1)
        GameEvent.validate_game_event(
            court=court.courtID,
            ball_game=TEST_BALL_GAME,
            min_number_of_players=2,
            max_number_of_players=10,
            time=time_now_plus_one_day)

    def test_game_event_create(self, court, court_ball_game):
        count_of_game_events = GameEvent.objects.count()
        time_now_plus_one_day = timezone.now() + timedelta(days=1)
        level_of_game = 5
        min_number_of_players = 2
        max_number_of_players = 5
        court = court
        ball_game = TEST_BALL_GAME
        GameEvent.create(
            time_now_plus_one_day,
            level_of_game,
            min_number_of_players,
            max_number_of_players,
            court, ball_game)
        assert GameEvent.objects.count() == count_of_game_events + 1

    def test_post_game_event(self, client, court, court_ball_game):
        count_of_game_events = GameEvent.objects.count()
        time_now_plus_one_day = (timezone.now() + timedelta(days=1)).strftime('%Y-%m-%dT%H:%M')
        response = client.post('/game-events/create/process', {
            'time': time_now_plus_one_day,
            'level_of_game': '5',
            'min_number_of_players': '3',
            'max_number_of_players': '10',
            'court': court.courtID,
            'ball_game': TEST_BALL_GAME,
        })
        assert GameEvent.objects.count() == count_of_game_events + 1
        assert response.status_code == 302
        assert response.url == '/game-events/'


@pytest.mark.django_db
class TestGameEventViews:

    def test_success_loading_site_game_event(self, client, saved_game_event, player):
        client.force_login(player.user)
        game_event_id = saved_game_event.id
        url = reverse('game_event', args=[game_event_id])
        response = client.get(url)
        assert response.status_code == 200

    def test_fail_loading_site_game_event(self, client, player):
        client.force_login(player.user)
        response = client.get('/game-events/-1/')
        assert response.status_code == 200
        assert b"Event Does not exist." in response.content

    def test_success_loading_site_join_game_event(self, client, saved_game_event, player):
        client.force_login(player.user)
        game_event_id = saved_game_event.id
        url = reverse('join_event', args=[game_event_id])
        response = client.get(url)
        assert response.status_code == 200

    def test_fail_loading_site_join_game_event(self, client, player):
        client.force_login(player.user)
        response = client.get('/game-events/join-event/-1/')
        assert response.status_code == 200
        assert b"Can not join, Event Does Not exist! " in response.content

    def test_success_loading_site_remove_game_event(self, client, saved_game_event, saved_game_event_player):
        client.force_login(saved_game_event_player.player.user)
        game_event_id = saved_game_event.id
        url = reverse('remove_from_event', args=[game_event_id])
        response = client.get(url)
        assert response.status_code == 200

    def test_fail_loading_site_remove_game_event_from_player(self, client, player):
        client.force_login(player.user)
        response = client.get('/game-events/remove-from-event/-1/')
        assert response.status_code == 200
        assert b"Can not remove from event, Event Does not Exist! " in response.content

    def test_fail_loading_remove_from_event_after_deleting_the_game_event(self, client, saved_game_event,
                                                                          saved_game_event_player):
        client.force_login(saved_game_event_player.player.user)
        game_event_id = saved_game_event.id
        url = reverse('remove_from_event', args=[game_event_id])
        response = client.get(url)
        assert response.status_code == 200
        saved_game_event.delete()
        response = client.get(url)
        assert response.status_code == 200
        assert b"Can not remove from event, Event Does not Exist! " in response.content

    def test_remove_player_from_event(self, client, saved_game_event, saved_game_event_player):
        client.force_login(saved_game_event_player.player.user)
        game_event_id = saved_game_event.id
        url = reverse('remove_from_event', args=[game_event_id])
        response = client.get(url)
        assert response.status_code == 200
        with pytest.raises(ObjectDoesNotExist):
            GameEventPlayer.objects.get(game_event=saved_game_event, player=saved_game_event_player.player)

    def test_remove_player_that_is_not_in_event(self, client, saved_game_event, player):
        client.force_login(player.user)
        game_event_id = saved_game_event.id
        url = reverse('remove_from_event', args=[game_event_id])
        with pytest.raises(ObjectDoesNotExist):
            client.get(url)

    def test_add_player_to_event(self, client, saved_game_event, player):
        client.force_login(player.user)
        game_event_id = saved_game_event.id
        url = reverse('process_answer_game_event', args=[game_event_id])
        response = client.post(url, {'answer': 'yes'})
        assert response.status_code == 200
        assert response.context['in_event']
        assert GameEventPlayer.objects.filter(game_event=saved_game_event, player=player).exists()

    def test_fail_add_player_to_event_already_in_it(self, client, saved_game_event, player):
        client.force_login(player.user)
        game_event_id = saved_game_event.id
        url = reverse('process_answer_game_event', args=[game_event_id])
        response = client.post(url, {'answer': 'yes'})
        assert response.status_code == 200
        with pytest.raises(IntegrityError):
            response = client.post(url, {'answer': 'yes'})
