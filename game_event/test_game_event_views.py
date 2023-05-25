import pytest
from django.urls import reverse
from .views import game_events


@pytest.mark.django_db
class TestGameEventServerResponses:

    def test_loading_site_no_filters(self, client):
        response = client.get('/game-events/')
        assert response.status_code == 200

    def test_fail_loading_site(self, client):
        response = client.get('/game-eventsss/')
        assert response.status_code == 404

    def test_shown_min_player_filter(self, client, game_event):
        response = client.get(reverse(game_events), {'min_players': '2'})
        assert response.status_code == 200
        game_events_response = response.context['game_events']
        assert any(game.id == game_event.id for game in game_events_response)

    def test_not_shown_min_player_filter(self, client, game_event):
        response = client.get(reverse(game_events), {'min_players': '10'})
        assert response.status_code == 200
        game_events_response = response.context['game_events']
        assert not any(game.id == game_event.id for game in game_events_response)

    def test_shown_max_player_filter(self, client, game_event):
        response = client.get(reverse(game_events), {'max_players': '15'})
        assert response.status_code == 200
        game_events_response = response.context['game_events']
        assert any(game.id == game_event.id for game in game_events_response)

    def test_not_shown_max_player_filter(self, client, game_event):
        response = client.get(reverse(game_events), {'max_players': '2'})
        assert response.status_code == 200
        game_events_response = response.context['game_events']
        assert not any(game.id == game_event.id for game in game_events_response)

    def test_shown_max_level_filter(self, client, game_event):
        response = client.get(reverse(game_events), {'max_level': '10'})
        assert response.status_code == 200
        game_events_response = response.context['game_events']
        assert any(game.id == game_event.id for game in game_events_response)

    def test_not_shown_max_level_filter(self, client, game_event):
        response = client.get(reverse(game_events), {'max_level': '2'})
        assert response.status_code == 200
        game_events_response = response.context['game_events']
        assert not any(game.id == game_event.id for game in game_events_response)
