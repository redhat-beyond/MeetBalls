from .models import Player, BallGame
from django.core.exceptions import ValidationError
import pytest


@pytest.mark.django_db
class TestPlayerModel:

    def test_get_player(self, player):
        player_from_db = Player.objects.get(pk=player.pk)
        assert player_from_db == player

    def test_update_player(self, player):
        player_copy = player
        assert player_copy.favorite_ball_game != BallGame.Basketball
        player_copy.favorite_ball_game = BallGame.Basketball
        player_copy.save()
        updated_player = Player.objects.get(pk=player_copy.pk)
        assert updated_player.favorite_ball_game == BallGame.Basketball

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
