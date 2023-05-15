import pytest
from django.urls import reverse
from .models import GameEvent, Court
from decimal import Decimal
from .views import game_events
from django.utils import timezone


@pytest.mark.django_db
class TestGameEventServerResponses:
    @pytest.fixture
    def saved_court(self):
        court = Court.objects.create(x=Decimal('11'), y=Decimal('22'),
                                     city='TEST_CITY', neighborhood='TEST_NEIGHBORHOOD', max_players=30)
        return court

    @pytest.fixture
    def saved_game_event(self, saved_court):
        game_event = GameEvent.objects.create(
            id=1000,
            time=timezone.now() - timezone.timedelta(days=1),
            level_of_game=5,
            min_number_of_players=4,
            max_number_of_players=10,
            court=saved_court,
            ball_game='Basketball'
        )
        return game_event

    def test_loading_site_no_filters(self, client):
        response = client.get('/game-events/')
        assert response.status_code == 200

    def test_fail_loading_site(self, client):
        response = client.get('/game-eventsss/')
        assert response.status_code == 404

    def test_shown_min_player_filter(self, client, saved_game_event):
        response = client.get(reverse(game_events), {'min_players': '2'})
        assert response.status_code == 200
        assert saved_game_event in response.context['game_events']

    def test_not_shown_min_player_filter(self, client, saved_game_event):
        response = client.get(reverse(game_events), {'min_players': '10'})
        assert response.status_code == 200
        assert saved_game_event not in response.context['game_events']

    def test_shown_max_player_filter(self, client, saved_game_event):
        response = client.get(reverse(game_events), {'max_players': '15'})
        assert response.status_code == 200
        assert saved_game_event in response.context['game_events']

    def test_not_shown_max_player_filter(self, client, saved_game_event):
        response = client.get(reverse(game_events), {'max_players': '2'})
        assert response.status_code == 200
        assert saved_game_event not in response.context['game_events']

    def test_shown_max_level_filter(self, client, saved_game_event):
        response = client.get(reverse(game_events), {'max_level': '10'})
        assert response.status_code == 200
        assert saved_game_event in response.context['game_events']

    def test_not_shown_max_level_filter(self, client, saved_game_event):
        response = client.get(reverse(game_events), {'max_level': '2'})
        assert response.status_code == 200
        assert saved_game_event not in response.context['game_events']
