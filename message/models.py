from django.db import models
from player.models import Player
from game_event.models import GameEvent
from django.core.validators import MinLengthValidator


class Message(models.Model):
    user_id = models.ForeignKey(Player, on_delete=models.CASCADE)
    game_event_id = models.ForeignKey(GameEvent, on_delete=models.CASCADE)
    time_sent = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=255, validators=[MinLengthValidator(1)])
