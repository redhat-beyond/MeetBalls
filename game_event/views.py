from .models import GameEvent
from django.shortcuts import render, redirect
from court.models import Court
from player_rating.models import Rating
from player.models import BallGame
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib import messages


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

        return redirect("/")  # will be changes later to "/game-events"
    else:
        return redirect("/game-events/create")
