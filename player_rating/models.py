from django.db import models
from player.models import BallGame, Player


# Zero will represent Free For all Game Event
class Rating(models.IntegerChoices):
    Zero = 0
    One = 1
    Two = 2
    Three = 3
    Four = 4
    Five = 5
    Six = 6
    Seven = 7
    Eight = 8
    Nine = 9
    Ten = 10


class PlayerRating(models.Model):
    ball_game = models.CharField(
        max_length=100,
        choices=BallGame.choices)
    player = models.ForeignKey(
        Player,
        on_delete=models.CASCADE)
    rating = models.IntegerField(choices=Rating.choices)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['ball_game', 'player'],
                name='unique_player_rating'
            )
        ]
        unique_together = ('ball_game', 'player')
