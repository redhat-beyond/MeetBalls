import datetime
from player.models import Player
import pytest
from django.urls import reverse
from django.utils import timezone


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
        username = "Player"
        password = "password"

        login_url = reverse('loginUser')
        response = client.post(
            login_url, {'username': username, 'password': password}, follow=True)

        assert response.redirect_chain[-1][0] == reverse('home')
        assert response.status_code == 200
        assert response.wsgi_request.user.is_authenticated is True
        assert response.wsgi_request.user.username == username

    @pytest.mark.parametrize('username, password', [
        ('wronguser', 'wrongpass'),
        ('Player', 'wrongpass'),
        ('wronguser', 'password'),
    ])
    def test_unsuccessful_login(self, client, username, password):
        login_url = reverse('loginUser')
        response = client.post(
            login_url, {'username': username, 'password': password})
        assert response.status_code == 200
        assert response.templates[0].name == 'meet_balls_app/login.html'
        assert response.wsgi_request.user.is_authenticated is False
        assert 'Invalid username or password.' in str(response.content)

    def test_register_navigation(self, client):
        login_url = reverse('loginUser')
        response = client.get(login_url, follow=True)
        assert response.status_code == 200
        register_url = reverse('registerUser')
        response = client.get(register_url)
        assert response.status_code == 200
        assert response.request['PATH_INFO'] == '/register/'


@pytest.mark.django_db
class Testlogout:
    def test_successful_logout(self, client, player):
        username = "daniel"
        password = "password"
        login_url = reverse('loginUser')
        client.post(login_url, {'username': username, 'password': password})
        logout_url = reverse('logoutUser')
        response = client.post(logout_url)
        assert response.status_code == 302
        assert response.url == reverse('home')
        assert response.wsgi_request.user.is_authenticated is False


@pytest.mark.django_db
class TestRegister:
    def test_successful_register(self, client):
        data = {
            'username': 'testuser',
            'password': 'testpassword',
            'confirm_password': 'testpassword',
            'birthdate': '1990-01-01',
            'favorite_ball_game': 'Soccer',
            'first_name': 'firstname',
            'last_name': 'lastname',
        }

        register_url = reverse('registerUser')
        response = client.post(register_url, data)
        assert Player.objects.filter(user__username='testuser').exists()
        assert response.status_code == 302
        assert response.url == reverse('loginUser')

    @pytest.mark.parametrize(
        'username, password, confirm_password, birthdate, favorite_ball_game, first_name, last_name', [
            ('', 'passwrod', 'password', '1990-01-01', 'Soccer', 'firstname', 'lastname'),
            ('testuser', '', 'password', '1990-01-01', 'Soccer', 'firstname', 'lastname'),
            ('testuser', 'password', '', '1990-01-01', 'Soccer', 'firstname', 'lastname'),
            ('testuser', 'password', 'password', '', 'Soccer', 'firstname', 'lastname'),
            ('testuser', 'password', 'password', '1990-01-01', '', 'firstname', 'lastname'),
            ('testuser', 'password', 'password', '1990-01-01', 'Soccer', '', 'lastname'),
            ('testuser', 'password', 'password', '1990-01-01', 'Soccer', 'firstname', ''),
        ])
    def test_unsuccessful_register_blank_field(
            self, client, username, password, confirm_password, birthdate, favorite_ball_game, first_name, last_name):
        data = {
            'username': username,
            'password': password,
            'confirm_password': confirm_password,
            'birthdate': birthdate,
            'favorite_ball_game': favorite_ball_game,
            'first_name': first_name,
            'last_name': last_name
        }
        response = client.post('/register/', data)

        assert response.status_code == 200
        assert 'All fields are required.' in response.content.decode()
        assert response.templates[0].name == 'meet_balls_app/register.html'

    def test_unsuccessful_register_user_is_already_exist(self, client):
        data = {
            'username': 'user1',
            'password': 'password',
            'confirm_password': 'password',
            'birthdate': '1990-01-01',
            'favorite_ball_game': 'Soccer'
        }
        response = client.post('/register/', data)

        assert response.status_code == 200
        assert 'Username already exists.' in response.content.decode()
        assert response.templates[0].name == 'meet_balls_app/register.html'

    def test_unsuccessful_register_passwords_dont_match(self, client):
        data = {
            'username': 'testuser',
            'password': 'password',
            'confirm_password': 'password1',
            'birthdate': '1990-01-01',
            'favorite_ball_game': 'Soccer',
        }

        response = client.post('/register/', data)

        assert response.status_code == 200
        assert 'Passwords do not match.' in response.content.decode()
        assert response.templates[0].name == 'meet_balls_app/register.html'

    def test_unsuccessful_register_birthdate_in_future(self, client):
        future_date = timezone.now() + datetime.timedelta(days=1)
        data = {
            'username': 'testuser',
            'password': 'password',
            'confirm_password': 'password',
            'birthdate': future_date.strftime('%Y-%m-%d'),
            'favorite_ball_game': 'Soccer',
        }

        response = client.post('/register/', data)

        assert response.status_code == 200
        assert 'Birthdate must be in the past.' in response.content.decode()
        assert response.templates[0].name == 'meet_balls_app/register.html'

    def test_unsuccessful_register_invalid_ball_game(self, client):
        data = {
            'username': 'testuser',
            'password': 'password',
            'confirm_password': 'password',
            'birthdate': '2000-01-01',
            'favorite_ball_game': 'InvalidBallGame',
        }

        response = client.post('/register/', data)

        assert response.status_code == 200
        assert 'Invalid ball game selection.' in response.content.decode()
        assert response.templates[0].name == 'meet_balls_app/register.html'

    def test_login_page_navigation(self, client):
        register_url = reverse('registerUser')
        response = client.get(register_url, follow=True)
        assert response.status_code == 200
        login_url = reverse('loginUser')
        response = client.get(login_url)
        assert response.status_code == 200
        assert response.request['PATH_INFO'] == '/login/'
