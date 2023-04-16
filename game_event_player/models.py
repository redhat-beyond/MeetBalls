from django.db import models
from player.models import Player
from game_event.models import GameEvent


class GameEventPlayer(models.Model):
    game_event_id = models.ForeignKey(GameEvent, on_delete=models.CASCADE)
    player_id = models.ForeignKey(Player, on_delete=models.CASCADE)
    ball_responsible = models.BooleanField(default=False)

    class Meta:
        unique_together = ('game_event_id', 'player_id')
