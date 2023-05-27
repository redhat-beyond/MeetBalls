from django.db import models
from player.models import Player
from game_event.models import GameEvent


class GameEventPlayer(models.Model):
    game_event = models.ForeignKey(GameEvent, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    ball_responsible = models.BooleanField(default=False)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['game_event', 'player'], name='unique_game_event_player')]
        unique_together = ('game_event', 'player')

    @staticmethod
    def remove_player_and_check_event_deletion(game_event, player):
        deleted = False
        GameEventPlayer.objects.get(game_event=game_event, player=player).delete()
        if not GameEventPlayer.objects.filter(game_event=game_event).exists():
            game_event.delete()
            deleted = True
        return deleted
