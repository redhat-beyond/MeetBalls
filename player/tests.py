from django.contrib.auth import get_user_model
from .models import Player, BallGame
from django.core.exceptions import ValidationError
import pytest


@pytest.mark.django_db
class TestPlayerModel:

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

    def test_get_player(self, saved_player):
        player = Player.objects.get(pk=saved_player.pk)
        assert player == saved_player

    def test_update_player(self, saved_player):
        player = saved_player
        assert player.favorite_ball_game != BallGame.Basketball
        player.favorite_ball_game = BallGame.Basketball
        player.save()
        updated_player = Player.objects.get(pk=player.pk)
        assert updated_player.favorite_ball_game == BallGame.Basketball

    def test_delete_player(self, saved_player):
        player = saved_player
        player.delete()
        with pytest.raises(Player.DoesNotExist):
            Player.objects.get(pk=saved_player.pk)

    def test_delete_user_deletes_player(self, saved_player):
        user = saved_player.user
        user.delete()
        with pytest.raises(Player.DoesNotExist):
            Player.objects.get(pk=saved_player.pk)

    def test_create_player_with_valid_fields(self, user):
        Player.objects.create(
            user=user,
            birth_date='1990-01-01',
            favorite_ball_game=BallGame.Soccer).full_clean()

    def test_create_player_with_invalid_birth_date(self, user):
        with pytest.raises(ValidationError):
            Player.objects.create(
                user=user,
                birth_date='invalid date',
                favorite_ball_game=BallGame.Soccer).full_clean()

    def test_create_player_with_invalid_favorite_ball_game(self, user):
        with pytest.raises(ValidationError):
            Player.objects.create(
                user=user,
                birth_date='1990-01-01',
                favorite_ball_game='invalid game').full_clean()

    def test_create_player_with_blank_birth_date(self, user):
        with pytest.raises(ValidationError):
            Player.objects.create(
                user=user,
                birth_date='',
                favorite_ball_game=BallGame.Soccer).full_clean()

    def test_create_player_with_blank_favorite_ball_game(self, user):
        with pytest.raises(ValidationError):
            Player.objects.create(
                user=user,
                birth_date='1990-01-01',
                favorite_ball_game='').full_clean()

    def test_create_player_with_null_favorite_ball_game(self, user):
        with pytest.raises(ValidationError):
            Player.objects.create(
                user=user,
                birth_date='1990-01-01',
            ).full_clean()
