from .models import CourtBallGame
from player.models import BallGame
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
import pytest


@pytest.mark.django_db
class TestCourtBallGameModel:

    def test_unique_together(self, court_ball_game):
        with pytest.raises(IntegrityError):
            CourtBallGame.objects.create(court=court_ball_game.court,
                                         ball_game=court_ball_game.ball_game)

    def test_create_court_ball_game(self, court_ball_game):
        assert isinstance(court_ball_game, CourtBallGame)

    def test_create_court_ball_game_invalid_court_id(self):
        with pytest.raises(IntegrityError):
            CourtBallGame.objects.create(court=None, ball_game=BallGame.Basketball)

    def test_create_court_ball_game_invalid_ball_game(self, court):
        with pytest.raises(ValidationError):
            CourtBallGame.objects.create(court=court, ball_game='Invalid-Ball-Game').full_clean()

    def test_update_court_ball_game(self, court_ball_game):
        court_ball_game.ball_game = BallGame.Volleyball
        court_ball_game.save()
        updated_court_ball_game = CourtBallGame.objects.get(id=court_ball_game.id)
        assert updated_court_ball_game.ball_game == BallGame.Volleyball

    def test_delete_court_ball_game(self, court_ball_game):
        court_ball_game.delete()
        with pytest.raises(CourtBallGame.DoesNotExist):
            CourtBallGame.objects.get(id=court_ball_game.id)

    def test_create_court_ball_game_with_blank_ball_game(self, court):
        with pytest.raises(ValidationError):
            CourtBallGame.objects.create(
                court=court,
                ball_game='').full_clean()

    def test_create_court_ball_game_with_null_ball_game(self, court):
        with pytest.raises(ValidationError):
            CourtBallGame.objects.create(
                court=court
            ).full_clean()

    def test_is_ball_game_playable(self, court, court_ball_game):
        assert CourtBallGame.is_ball_game_playable(court, BallGame.Basketball)

    def test_is_ball_game_playable_false(self, court):
        expected = False
        assert expected == CourtBallGame.is_ball_game_playable(court, BallGame.Basketball)
