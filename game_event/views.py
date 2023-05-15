from .models import GameEvent
from django.shortcuts import render, redirect
from court.models import Court
from player_rating.models import Rating
from player.models import BallGame
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib import messages
from datetime import date


def display_game_event_form(request):
    courts = Court.objects.all()
    return render(request, 'game_event/game_event_form.html', {
        'courts': courts,
        'ratings': Rating.choices,
        'games': BallGame.choices
    })


def process_game_event_form(request):
    if request.method == 'POST':
        time_str = request.POST.get('time')
        time = timezone.datetime.fromisoformat(time_str)
        time = timezone.make_aware(time)
        level_of_game = request.POST.get('level_of_game')
        min_number_of_players = int(request.POST.get('min_number_of_players'))
        max_number_of_players = int(request.POST.get('max_number_of_players'))
        court_id = request.POST.get('court')
        court = Court.objects.get(courtID=court_id)
        ball_game = request.POST.get('ball_game')

        try:
            GameEvent.create(time, level_of_game, min_number_of_players, max_number_of_players, court, ball_game)
        except ValidationError as e:
            error_messages = e.messages[0].split("\n")
            for error in error_messages:
                messages.error(request, error)
            return redirect("/game-events/create")

        return redirect("/game-events/")
    else:
        return redirect("/game-events/create")


def game_events(request):
    game_events = GameEvent.objects.all()

    if request.GET.get('min_players'):
        min_players = int(request.GET.get('min_players'))
        game_events = game_events.filter(min_number_of_players__gte=min_players)

    if request.GET.get('max_players'):
        max_players = int(request.GET.get('max_players'))
        game_events = game_events.filter(max_number_of_players__lte=max_players)

    if request.GET.get('max_level'):
        max_level = int(request.GET.get('max_level'))
        game_events = game_events.filter(level_of_game__lte=max_level)

    if request.GET.get('hide_past_events'):
        current_date = date.today()
        game_events = game_events.filter(time__gte=current_date)

    return render(request, 'game-events.html', {'game_events': game_events})
