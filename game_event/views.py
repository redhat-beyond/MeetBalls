from .models import GameEvent
from django.shortcuts import render, redirect
from court.models import Court
from game_event_player.models import GameEventPlayer
from player_rating.models import Rating
from player.models import BallGame, Player
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib import messages
from message.models import Message
from datetime import date
import urllib.request
import json
import os


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
            player = Player.objects.get(user=request.user)
            event = GameEvent.create(time, level_of_game, min_number_of_players,
                                     max_number_of_players, court, ball_game)
            GameEventPlayer.objects.create(game_event=event, player=player, ball_responsible=False)
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

    game_events = get_weather_from_api(game_events, urllib.request.urlopen)

    return render(request, 'game-events.html', {'game_events': game_events})


def game_event(request, id):
    try:
        event = GameEvent.objects.get(pk=id)
    except GameEvent.DoesNotExist:
        return render(request, 'game_event/game-event.html', {})
    try:
        player = Player.objects.get(user=request.user)
    except Player.DoesNotExist:
        context = {
            'id': event.id,
            'time': event.time,
            'level_of_game': event.level_of_game,
            'min_number_of_players': event.min_number_of_players,
            'max_number_of_players': event.max_number_of_players,
            'court': event.court.city,
            'neighborhood': event.court.neighborhood,
            'ball_game': event.ball_game,
            'in_event': False,
        }
        return render(request, 'game_event/game-event.html', context)

    event_players = [
        {
            "first_name": entry.player.user.first_name,
            "last_name": entry.player.user.last_name,
            "brings_ball": entry.ball_responsible,
        }
        for entry in GameEventPlayer.objects.filter(game_event=event)
    ]
    in_event = GameEventPlayer.objects.filter(game_event=event, player=player).exists()
    all_messages = Message.objects.filter(game_event_id=event)
    context = {
        'id': event.id,
        'time': event.time,
        'level_of_game': event.level_of_game,
        'min_number_of_players': event.min_number_of_players,
        'max_number_of_players': event.max_number_of_players,
        'court': event.court.city,
        'neighborhood': event.court.neighborhood,
        'ball_game': event.ball_game,
        'in_event': in_event,
        'event_players': event_players,
        'all_messages': all_messages
        }
    return render(request, 'game_event/game-event.html', context)


def join_event(request, id):
    try:
        GameEvent.objects.get(pk=id)
    except GameEvent.DoesNotExist:
        return render(request, 'game_event/join-event.html', {'id': id, 'event_exists': False})

    return render(request, 'game_event/join-event.html', {'id': id, 'event_exists': True})


def remove_from_event(request, id):
    try:
        event = GameEvent.objects.get(pk=id)
    except GameEvent.DoesNotExist:
        return render(request, 'game_event/result.html', {'event_exists': False})
    player = Player.objects.get(user=request.user)
    GameEventPlayer.remove_player_and_check_event_deletion(event, player)
    return render(request, 'game_event/result.html')


def process_answer_game_event(request, id):
    try:
        event = GameEvent.objects.get(pk=id)
    except GameEvent.DoesNotExist:
        return render(request, 'game_event/result.html', {'event_exists': False})

    player = Player.objects.get(user=request.user)
    ball_responsible = request.POST.get('answer') == 'yes'
    content = {}
    num_of_players_in_event = len(GameEventPlayer.objects.filter(game_event=event))
    if num_of_players_in_event < event.max_number_of_players:
        GameEventPlayer.objects.create(game_event=event, player=player, ball_responsible=ball_responsible).save()
        in_event = GameEventPlayer.objects.filter(game_event=event, player=player).exists()
        content["in_event"] = in_event
        content["reached_max"] = False
    else:
        content["reached_max"] = True
    content['event_exists'] = True

    return render(request, 'game_event/result.html', content)


def get_weather_from_api(game_events, weather_getter):
    url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {'units': 'metric', 'appid': os.getenv("APPID")}
    for game in game_events:

        params['q'] = game.court.city

        full_url = url + '?' + urllib.parse.urlencode(params)
        try:
            response = weather_getter(full_url)
        except Exception:
            game.weather = None
            continue

        if response.status == 200:
            data = response.read().decode('utf-8')
            weather_data = json.loads(data)
            curr_icon = weather_data['weather'][0]['icon']
            icon_url = "http://openweathermap.org/img/wn/" + curr_icon + "@2x.png"
            curr_temp = weather_data['main']['temp']
            game.weather = {'icon': icon_url, 'temp': curr_temp}
        else:
            game.weather = None

    return game_events
