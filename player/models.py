from django.contrib.auth.models import User
from django.db import models
import datetime
from django.core.exceptions import ValidationError
from django.utils import timezone


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


def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class Player(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True)
    birth_date = models.DateField()
    favorite_ball_game = models.CharField(
        max_length=100,
        choices=BallGame.choices)
    profile_pic = models.ImageField(default='default-profile-pic.png', upload_to=user_directory_path)

    @staticmethod
    def create(username, password, birth_date, favorite_ball_game):
        player = Player(user=User.objects.create_user(
                    username=username,
                    password=password), birth_date=birth_date, favorite_ball_game=favorite_ball_game)
        player.user.save()
        player.save()
        return player

    def validate_and_save(self, birth_date, favorite_ball_game, profile_picture=None):
        errors = []
        try:
            datetime.datetime.strptime(birth_date, '%Y-%m-%d').date()
            self.birth_date = birth_date
        except ValueError:
            errors.append("Invalid birth date format, Please use the format YYYY-MM-DD.")

        ball_games_names = [choice[0] for choice in BallGame.choices]
        if favorite_ball_game not in ball_games_names:
            errors.append("Invalid favorite ball game, Please select a valid option.")
        else:
            self.favorite_ball_game = favorite_ball_game

        if profile_picture:
            if not profile_picture.name.lower().endswith(('.png', '.jpeg', '.jpg')):
                errors.append("Invalid picture format, Please upload a JPEG or PNG image.")
            else:
                self.profile_pic.save(profile_picture.name, profile_picture, save=False)

        if errors:
            raise ValidationError("\n".join(errors))

        else:
            self.save()

    def is_event_time_available(self, desired_event_time):
        from game_event_player.models import GameEventPlayer
        TIME_LIMIT = 4
        start_time_limit = desired_event_time - timezone.timedelta(hours=TIME_LIMIT)
        end_time_limit = desired_event_time + timezone.timedelta(hours=TIME_LIMIT)
        conflicting_events = GameEventPlayer.objects.filter(player=self,
                                                            game_event__time__range=(start_time_limit,
                                                                                     end_time_limit))
        return not conflicting_events.exists()
