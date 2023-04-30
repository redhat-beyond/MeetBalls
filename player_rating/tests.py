from .models import PlayerRating, Rating
from player.models import BallGame, Player
from django.core.exceptions import ValidationError
from django.db import IntegrityError
import pytest


@pytest.mark.django_db
class TestPlayerRatingModel:

    @pytest.fixture
    def player_rating(self, player):
        player_rating_fixture = PlayerRating.objects.create(
            ball_game=BallGame.Soccer,
            player=player,
            rating=Rating.Five
        )
        return player_rating_fixture

    def test_get_player_rating(self, player_rating):
        player_rating_from_db = PlayerRating.objects.get(
            pk=player_rating.pk)
        assert player_rating_from_db == player_rating

    def test_update_player_rating(self, player_rating):
        assert player_rating.rating != Rating.Seven
        player_rating.rating = Rating.Seven
        player_rating.save()
        updated_player_rating = PlayerRating.objects.get(
            ball_game=BallGame.Soccer,
            player=player_rating.player)
        assert updated_player_rating.rating == Rating.Seven

    def test_delete_player_rating(self, player_rating):
        player_rating.delete()
        with pytest.raises(PlayerRating.DoesNotExist):
            PlayerRating.objects.get(
                ball_game=BallGame.Soccer,
                player=player_rating.player)

    def test_create_player_rating_invalid_ball_game(self, player_rating):
        with pytest.raises(ValidationError):
            PlayerRating.objects.create(
                ball_game='Invalid Ball Game',
                player=player_rating.player,
                rating=Rating.Five).full_clean()

    def test_create_player_rating_invalid_user_id(self):
        with pytest.raises(IntegrityError):
            PlayerRating.objects.create(
                ball_game=BallGame.Soccer,
                player=None,
                rating=Rating.Five)

    def test_create_player_rating_invalid_rating(self, player_rating):
        with pytest.raises(IntegrityError):
            PlayerRating.objects.create(
                ball_game=BallGame.Soccer,
                player=player_rating.player)

    def test_create_player_rating_invalid_rating2(self, player_rating):
        with pytest.raises(IntegrityError):
            PlayerRating.objects.create(
                ball_game=BallGame.Soccer,
                player=player_rating.player,
                rating=0)

    def test_delete_player_deletes_player_ratings(self, player, player_rating):
        assert Player.objects.count() == 1
        assert PlayerRating.objects.count() == 1
        player.delete()
        assert Player.objects.count() == 0
        assert PlayerRating.objects.count() == 0

    def test_create_valid_player_rating(self, player):
        PlayerRating.objects.create(
            ball_game=BallGame.Baseball,
            player=player,
            rating=Rating.Eight).full_clean()

    def test_create_duplicate_player_rating(self, player_rating):
        with pytest.raises(IntegrityError):
            PlayerRating.objects.create(
                ball_game=player_rating.ball_game,
                player=player_rating.player,
                rating=Rating.Five
            )
