from django.db import models
from player.models import Player
from game_event.models import GameEvent
from game_event_player.models import GameEventPlayer
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError


class Message(models.Model):
    user_id = models.ForeignKey(Player, on_delete=models.CASCADE)
    game_event_id = models.ForeignKey(GameEvent, on_delete=models.CASCADE)
    time_sent = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=255, validators=[MinLengthValidator(1)])

    @staticmethod
    def create(player, game_event, text):
        Message.validate_message(player, game_event, text)
        message = Message(user_id=player,
                          game_event_id=game_event,
                          text=text)

        message.save()
        return message

    @staticmethod
    def validate_message(player, game_event, text):
        game_event = GameEvent.objects.get(pk=game_event.pk)
        player_participates = GameEventPlayer.objects.filter(player=player, game_event=game_event).exists()
        errors = []
        if player_participates is False:
            errors.append("Just players from this event can send messages on chat")
        if text.strip() == '':
            errors.append("Message can't be empty")

        if errors:
            raise ValidationError("\n".join(errors))
