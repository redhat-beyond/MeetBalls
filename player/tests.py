from .models import Player, BallGame
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db import IntegrityError
import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
import os
from django.conf import settings
from player.models import user_directory_path


@pytest.mark.django_db
class TestPlayerModel:

    def test_get_player(self, player):
        player_from_db = Player.objects.get(pk=player.pk)
        assert player_from_db == player

    def test_update_player(self, player):
        assert player.favorite_ball_game != BallGame.Basketball
        player.favorite_ball_game = BallGame.Basketball
        player.save()
        updated_player = Player.objects.get(pk=player.pk)
        assert updated_player.favorite_ball_game == BallGame.Basketball

    def test_create_player_with_new_user(self):
        player = Player.create(username='daniel',
                               password='password',
                               birth_date='1990-01-01',
                               favorite_ball_game=BallGame.Soccer)
        assert isinstance(player.user, User)
        assert player.user.username == 'daniel'
        assert player.user.check_password('password')

    def test_create_player_with_existing_username(self):
        user = User.objects.create_user(username='daniel', password='password')
        user.save()
        with pytest.raises(IntegrityError):
            Player.create(
                username=user.username,
                password=user.password,
                birth_date='1990-01-01',
                favorite_ball_game=BallGame.Soccer)

    def test_delete_player(self, player):
        player_copy = player
        player_copy.delete()
        with pytest.raises(Player.DoesNotExist):
            Player.objects.get(pk=player.pk)

    def test_delete_user_deletes_player(self, player):
        user = player.user
        user.delete()
        with pytest.raises(Player.DoesNotExist):
            Player.objects.get(pk=player.pk)

    def test_create_player_with_valid_fields(self):
        Player.create(
            username="daniel",
            password="password",
            birth_date='1990-01-01',
            favorite_ball_game=BallGame.Soccer).full_clean()

    def test_create_player_with_invalid_birth_date(self):
        with pytest.raises(ValidationError):
            Player.create(
                username="daniel",
                password="password",
                birth_date='invalid date',
                favorite_ball_game=BallGame.Soccer).full_clean()

    def test_create_player_with_invalid_favorite_ball_game(self):
        with pytest.raises(ValidationError):
            Player.create(
                username="daniel",
                password="password",
                birth_date='1990-01-01',
                favorite_ball_game='invalid game').full_clean()

    def test_create_player_with_blank_birth_date(self):
        with pytest.raises(ValidationError):
            Player.create(
                username="daniel",
                password="password",
                birth_date='',
                favorite_ball_game=BallGame.Soccer).full_clean()

    def test_create_player_with_blank_favorite_ball_game(self):
        with pytest.raises(ValidationError):
            Player.create(
                username="daniel",
                password="password",
                birth_date='1990-01-01',
                favorite_ball_game='').full_clean()

    def test_create_player_with_null_favorite_ball_game(self):
        with pytest.raises(IntegrityError):
            Player.create(
                username="daniel",
                password="password",
                birth_date='1990-01-01',
                favorite_ball_game=None,
            )

    def test_validate_and_save_valid_data(self, player):
        birth_date = '1999-02-01'
        favorite_ball_game = BallGame.Basketball

        assert player.birth_date != birth_date
        assert player.favorite_ball_game != favorite_ball_game

        profile_pic = SimpleUploadedFile("sample.jpg", b"dummy_image_data", content_type="image/jpeg")
        player.validate_and_save(birth_date, favorite_ball_game, profile_pic)

        assert player.birth_date == birth_date
        assert player.favorite_ball_game == favorite_ball_game
        expected_file_path = os.path.join(settings.MEDIA_ROOT, player.profile_pic.name)
        assert os.path.exists(expected_file_path)

    @pytest.mark.parametrize(
        "birth_date, favorite_ball_game, profile_pic, expected_errors",
        [
            ('1990-05-05', "InvalidBallGame",
             SimpleUploadedFile("test_image.jpg", b"dummy_image_data", content_type="image/jpeg"),
             ["Invalid favorite ball game",]),
            ('invalid_date', BallGame.Soccer,
             SimpleUploadedFile("test_image.jpg", b"dummy_image_data", content_type="image/jpeg"),
             ["Invalid birth date format",]),
            ('invalid_date', "InvalidBallGame",
             SimpleUploadedFile("test_image.jpg", b"dummy_image_data", content_type="image/jpeg"),
             ["Invalid favorite ball game", "Invalid birth date format"]),
            ('invalid_date', BallGame.Basketball, None,
             ["Invalid birth date format",]),
            ('1999-01-01', 'InvalidBallGame', None,
             ["Invalid favorite ball game",]),
            ('invalid_date', 'InvalidBallGame', None,
             ["Invalid favorite ball game", "Invalid birth date format"]),
            ('2000-01-01', BallGame.Basketball,
             SimpleUploadedFile("test_image.txt", b"dummy_file_data", content_type="image/jpeg"),
             ["Invalid picture format",]),
            ('2000-01-01', "InvalidBallGame",
             SimpleUploadedFile("test_image.txt", b"dummy_image_data", content_type="image/jpeg"),
             ["Invalid favorite ball game", "Invalid picture format",]),
            ("invalid_date", BallGame.Basketball,
             SimpleUploadedFile("test_image.txt", b"dummy_image_data", content_type="image/jpeg"),
             ["Invalid birth date format", "Invalid picture format",]),
        ]
    )
    def test_validate_and_save_invalid_inputs(self, player, birth_date, favorite_ball_game, profile_pic,
                                              expected_errors):
        with pytest.raises(ValidationError) as e:
            player.validate_and_save(birth_date, favorite_ball_game, profile_pic)

            for error in expected_errors:
                assert error in str(e.value)


@pytest.mark.django_db
class TestUserDirectoryPath:
    def test_user_directory_path(self, player):
        filename = 'example.jpg'
        result = user_directory_path(player, filename)
        expected_output = f'user_{player.user.id}/example.jpg'
        assert result == expected_output
