from django.db import models
from court.models import Court
from player.models import BallGame


class CourtBallGame(models.Model):
    court = models.ForeignKey(Court, on_delete=models.CASCADE)
    ball_game = models.CharField(
        max_length=100,
        choices=BallGame.choices
    )

    class Meta:
        unique_together = ('court', 'ball_game')

    @staticmethod
    def is_ball_game_playable(court, ball_game):
        ball_games_available_at_court = CourtBallGame.objects.filter(court=court)
        return any(bg.ball_game == ball_game for bg in ball_games_available_at_court)
