from django.db import models
from django.core.validators import MinLengthValidator
from court.models import Court
from player_rating.models import Rating


class BallGame(models.TextChoices):
    Soccer = 'Soccer', 'Soccer'
    Basketball = 'Basketball', 'Basketball'
    Volleyball = 'Volleyball', 'Volleyball'
    Baseball = 'Baseball', 'Baseball'
    Tennis = 'Tennis', 'Tennis'
    Rugby = 'Rugby', 'Rugby'
    Golf = 'Golf', 'Golf'
    Cricket = 'Cricket', 'Cricket'
    Handball = 'Handball', 'Handball'


class GameEvent(models.Model):
    id = models.IntegerField(primary_key=True)
    time = models.DateTimeField(null=False)
    level_of_game = models.IntegerField(choices=Rating.choices, blank=True)
    min_number_of_players = models.PositiveIntegerField()
    max_number_of_players = models.PositiveIntegerField()
    court_id = models.ForeignKey(Court, on_delete=models.CASCADE)
    ball_game = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(4)],
        choices=BallGame.choices
    )
