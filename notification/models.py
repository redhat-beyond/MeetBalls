from django.db import models
from django.utils import timezone
from player.models import Player


class NotificationType(models.TextChoices):
    WEBSITE = "website", "Website"
    EVENT = "game-event", "Game-Event"
    CHAT = "chat", "Chat"


class Notification(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    sent_time = models.DateTimeField(default=timezone.now)
    message = models.TextField(null=True, blank=True)
    notification_type = models.CharField(
        max_length=100,
        choices=NotificationType.choices,
        default=NotificationType.WEBSITE,
    )
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.notification_type} - {self.message}"

    def mark_notification_as_read(self):
        self.is_read = True
        self.save()
