from django.db import models
from django.core.validators import MinLengthValidator
from court.models import Court
from player_rating.models import Rating
from player.models import BallGame
from court_ball_game.models import CourtBallGame
from django.utils import timezone
from django.core.exceptions import ValidationError
import datetime


class GameEvent(models.Model):
    time = models.DateTimeField(null=False)
    level_of_game = models.IntegerField(choices=Rating.choices, blank=True)
    min_number_of_players = models.PositiveIntegerField()
    max_number_of_players = models.PositiveIntegerField()
    court = models.ForeignKey(Court, on_delete=models.CASCADE)
    ball_game = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(4)],
        choices=BallGame.choices
    )

    @staticmethod
    def create(time, level_of_game, min_number_of_players, max_number_of_players, court, ball_game):
        GameEvent.validate_game_event(court, ball_game, min_number_of_players, max_number_of_players, time)
        game_event = GameEvent(time=time,
                               level_of_game=level_of_game,
                               min_number_of_players=min_number_of_players,
                               max_number_of_players=max_number_of_players,
                               court=court,
                               ball_game=ball_game)

        game_event.save()
        return game_event

    @staticmethod
    def validate_game_event(court, ball_game, min_number_of_players, max_number_of_players, time):
        errors = []
        if not GameEvent.is_ball_game_playable_at_court(court, ball_game):
            errors.append("The selected court doesn't support the selected ball game.")
        if min_number_of_players < 2:
            errors.append("The minimum number of players must be at least 2.")
        if max_number_of_players < min_number_of_players:
            errors.append("The maximum number of players must be at least equal to the minimum number of players")
        if time < timezone.now() or time > timezone.now() + datetime.timedelta(days=30):
            errors.append("The selected time must be between now and one month from now.")
        if errors:
            raise ValidationError("\n".join(errors))

    @staticmethod
    def is_ball_game_playable_at_court(court, ball_game):
        return CourtBallGame.is_ball_game_playable(court, ball_game)
