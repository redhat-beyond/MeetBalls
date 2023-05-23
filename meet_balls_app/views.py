from datetime import datetime
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages
from player.models import BallGame, Player
from django.contrib.auth.models import User


def home(request):
    return render(request, 'meet_balls_app/home.html')


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
