from .models import CourtBallGame
from court.models import Court
from player.models import BallGame
from decimal import Decimal
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
import pytest


@pytest.mark.django_db
class TestCourtBallGameModel:

    @pytest.fixture
    def court_instance(self):
        court = Court.objects.create(courtID=1, x=Decimal('11'), y=Decimal('22'),
                                     city='TEST_CITY', neighborhood='TEST_NEIGHBORHOOD', max_players=30)
        return court

    @pytest.fixture
    def court_ball_game_instance(self, court_instance):
        court_ball_game = CourtBallGame.objects.create(court=court_instance, ball_game=BallGame.Basketball)
        return court_ball_game

    def test_unique_together(self, court_ball_game_instance):
        with pytest.raises(IntegrityError):
            CourtBallGame.objects.create(court=court_ball_game_instance.court,
                                         ball_game=court_ball_game_instance.ball_game)

    def test_create_court_ball_game(self, court_ball_game_instance):
        assert isinstance(court_ball_game_instance, CourtBallGame)

    def test_create_court_ball_game_invalid_court_id(self):
        with pytest.raises(IntegrityError):
            CourtBallGame.objects.create(court=None, ball_game=BallGame.Basketball)

    def test_create_court_ball_game_invalid_ball_game(self, court_instance):
        with pytest.raises(ValidationError):
            CourtBallGame.objects.create(court=court_instance, ball_game='Invalid-Ball-Game').full_clean()

    def test_update_court_ball_game(self, court_ball_game_instance):
        court_ball_game_instance.ball_game = BallGame.Volleyball
        court_ball_game_instance.save()
        updated_court_ball_game = CourtBallGame.objects.get(id=court_ball_game_instance.id)
        assert updated_court_ball_game.ball_game == BallGame.Volleyball

    def test_delete_court_ball_game(self, court_ball_game_instance):
        court_ball_game_instance.delete()
        with pytest.raises(CourtBallGame.DoesNotExist):
            CourtBallGame.objects.get(id=court_ball_game_instance.id)

    def test_create_court_ball_game_with_blank_ball_game(self, court_instance):
        with pytest.raises(ValidationError):
            CourtBallGame.objects.create(
                court=court_instance,
                ball_game='').full_clean()

    def test_create_court_ball_game_with_null_ball_game(self, court_instance):
        with pytest.raises(ValidationError):
            CourtBallGame.objects.create(
                court=court_instance
            ).full_clean()
