import pytest
from django.urls import reverse


class TestUi:

    def test_home_page_extends_base(self, client):
        response = client.get('/')
        assert response.status_code == 200
        assert b'<nav' in response.content
        assert b'Login' in response.content

    @pytest.mark.django_db
    def test_logged_user_see_logout_in_navbar(self, client, player):
        client.force_login(player.user)
        response = client.get('/')
        assert response.status_code == 200
        assert b'<nav' in response.content
        assert b'Logout' in response.content

    @pytest.mark.django_db
    def test_display_game_event_form(self, client):
        response = client.get('/game-events/create/')
        assert response.status_code == 200
        assert b'<form' in response.content


@pytest.mark.django_db
class Testlogin:
    def test_successful_login(self, client, player):
        username = "daniel"
        password = "password"

        login_url = reverse('loginUser')
        response = client.post(
            login_url, {'username': username, 'password': password})

        assert response.templates[0].name == 'meet_balls_app/home.html'
        assert response.status_code == 200
        assert response.context['user']['is_authenticated'] is True
        assert response.context['user']['username'] == username

    @pytest.mark.parametrize('username, password', [
        ('wronguser', 'wrongpass'),
        ('daniel', 'wrongpass'),
        ('wronguser', 'password'),
    ])
    def test_unsuccessful_login(self, client, username, password):
        login_url = reverse('loginUser')
        response = client.post(
            login_url, {'username': username, 'password': password})
        assert response.status_code == 200
        assert response.templates[0].name == 'meet_balls_app/login.html'
        assert response.context['user']['is_authenticated'] is False
        assert 'Invalid username or password.' in str(response.content)


@pytest.mark.django_db
class Testlogout:
    def test_successful_logout(self, client, player):
        username = "daniel"
        password = "password"
        login_url = reverse('loginUser')
        client.post(login_url, {'username': username, 'password': password})
        logout_url = reverse('logoutUser')
        response = client.post(logout_url)
        assert response.status_code == 200
        assert response.templates[0].name == 'meet_balls_app/home.html'
        assert response.context['user']['is_authenticated'] is False
