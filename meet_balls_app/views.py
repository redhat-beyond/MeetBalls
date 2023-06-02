from django.shortcuts import render, redirect
from datetime import datetime
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages
from player.models import BallGame, Player
from django.contrib.auth.models import User
from player_rating.models import PlayerRating
from game_event_player.models import GameEventPlayer
from notification.models import Notification
from django.db.models import Count
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'meet_balls_app/home.html')

def notifications(request):
    notifications = Notification.objects.filter(player=request.user.player)

    context = {
        'notifications': notifications
    }

    return render(request, 'meet_balls_app/notifications.html', context)

def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error_message = "Invalid username or password."
            messages.error(request, error_message)
            return render(request, 'meet_balls_app/login.html')
    else:
        return render(request, 'meet_balls_app/login.html')


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        birthdate = request.POST.get('birthdate')
        favorite_ball_game = request.POST.get('favorite_ball_game')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        data = {
            'username': username,
            'password': password,
            'confirm_password': confirm_password,
            'birthdate': birthdate,
            'favorite_ball_game': favorite_ball_game,
            'first_name': first_name,
            'last_name': last_name,
        }
        errors = validate_register_form(data)
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'meet_balls_app/register.html',
                          {'ball_games': BallGame.choices})
        else:
            try:
                Player.create(
                    username, password, birthdate, favorite_ball_game)
                messages.error(request, '')
                user = User.objects.get(username=username)
                user.first_name = first_name
                user.last_name = last_name
                user.save()
                return redirect('loginUser')
            except ValidationError as e:
                error_messages = e.messages[0].split("\n")
                for error in error_messages:
                    messages.error(request, error)
                    return render(request, "/meet_balls_app/register.html", {'ball_games': BallGame.choices})
    else:
        messages.error(request, '')
        return render(request, 'meet_balls_app/register.html', {'ball_games': BallGame.choices})


def validate_register_form(data):
    errors = []

    if not (data['username'] and data['password'] and
            data['confirm_password'] and data['birthdate'] and
            data['favorite_ball_game'] and data['first_name'] and data['last_name']):
        errors.append("All fields are required.")
    if data['password'] != data['confirm_password']:
        errors.append("Passwords do not match.")
    if User.objects.filter(username=data['username']).exists():
        errors.append("Username already exists.")
    if not any(data['favorite_ball_game'] in choice for choice in BallGame.choices):
        errors.append("Invalid ball game selection.")
    try:
        birthdate = datetime.strptime(data['birthdate'], '%Y-%m-%d').date()
        if birthdate >= datetime.now().date():
            errors.append("Birthdate must be in the past.")
    except ValueError:
        errors.append("Invalid birthdate format.")

    return errors


@login_required(login_url="/login/")
def profile(request, id):
    try:
        player = Player.objects.get(user=id)
    except Player.DoesNotExist:
        return render(request, 'meet_balls_app/profile.html', {})
    ratings = PlayerRating.objects.filter(player=player)

    game_counts = GameEventPlayer.objects.filter(player=player).values('game_event__ball_game').annotate(
        count=Count('game_event__ball_game'))
    game_history_data = {item['game_event__ball_game']: item['count'] for item in game_counts}

    return render(request, 'meet_balls_app/profile.html',
                  {'player': player, 'ratings': ratings, 'game_history_data': game_history_data, 'url_id': id})


@login_required(login_url="/login/")
def edit_profile(request):
    player = Player.objects.get(user=request.user.id)
    ratings = PlayerRating.objects.filter(player=player)
    if request.method == 'POST':
        birth_date = request.POST.get('birth_date')
        favorite_ball_game = request.POST.get('favorite_ball_game')
        try:
            player.validate_and_save(birth_date, favorite_ball_game)
            for rating in ratings:
                rating_value = request.POST.get(f"rating[{rating.id}]")
                rating.rating = int(rating_value)
                rating.save()
            return redirect('profile', id=player.user.id)
        except ValidationError as e:
            error_messages = e.messages[0].split("\n")
            for error in error_messages:
                messages.error(request, error)
            return redirect("edit profile")
    else:
        return render(request, 'meet_balls_app/edit_profile_form.html', {
            "player": player,
            "ratings": ratings,
            "ball_games": BallGame.choices})
