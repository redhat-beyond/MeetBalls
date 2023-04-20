from .models import Player, BallGame
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db import IntegrityError
import pytest


@pytest.mark.django_db
class TestPlayerModel:

    def test_get_player(self, player):
        player_from_db = Player.objects.get(pk=player.pk)
        assert player_from_db == player

    def test_update_player(self, player):
        assert player.favorite_ball_game != BallGame.Basketball
        player.favorite_ball_game = BallGame.Basketball
        player.save()
        updated_player = Player.objects.get(pk=player.pk)
        assert updated_player.favorite_ball_game == BallGame.Basketball

    def test_create_player_with_new_user(self):
        player = Player.create(username='daniel',
                               password='password',
                               birth_date='1990-01-01',
                               favorite_ball_game=BallGame.Soccer)
        assert isinstance(player.user, User)
        assert player.user.username == 'daniel'
        assert player.user.check_password('password')

    def test_create_player_with_existing_username(self):
        user = User.objects.create_user(username='daniel', password='password')
        user.save()
        with pytest.raises(IntegrityError):
            Player.create(
                username=user.username,
                password=user.password,
                birth_date='1990-01-01',
                favorite_ball_game=BallGame.Soccer)

    def test_delete_player(self, player):
        player_copy = player
        player_copy.delete()
        with pytest.raises(Player.DoesNotExist):
            Player.objects.get(pk=player.pk)

    def test_delete_user_deletes_player(self, player):
        user = player.user
        user.delete()
        with pytest.raises(Player.DoesNotExist):
            Player.objects.get(pk=player.pk)

    def test_create_player_with_valid_fields(self):
        Player.create(
            username="daniel",
            password="password",
            birth_date='1990-01-01',
            favorite_ball_game=BallGame.Soccer).full_clean()

    def test_create_player_with_invalid_birth_date(self):
        with pytest.raises(ValidationError):
            Player.create(
                username="daniel",
                password="password",
                birth_date='invalid date',
                favorite_ball_game=BallGame.Soccer).full_clean()

    def test_create_player_with_invalid_favorite_ball_game(self):
        with pytest.raises(ValidationError):
            Player.create(
                username="daniel",
                password="password",
                birth_date='1990-01-01',
                favorite_ball_game='invalid game').full_clean()

    def test_create_player_with_blank_birth_date(self):
        with pytest.raises(ValidationError):
            Player.create(
                username="daniel",
                password="password",
                birth_date='',
                favorite_ball_game=BallGame.Soccer).full_clean()

    def test_create_player_with_blank_favorite_ball_game(self):
        with pytest.raises(ValidationError):
            Player.create(
                username="daniel",
                password="password",
                birth_date='1990-01-01',
                favorite_ball_game='').full_clean()

    def test_create_player_with_null_favorite_ball_game(self):
        with pytest.raises(IntegrityError):
            Player.create(
                username="daniel",
                password="password",
                birth_date='1990-01-01',
                favorite_ball_game=None,
            )
