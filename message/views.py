from django.shortcuts import render, redirect
from game_event.models import GameEvent
from player.models import Player
from .models import Message
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.contrib import messages


@login_required(login_url="/login/")
def save_text_message(request, id):
    try:
        event = GameEvent.objects.get(pk=id)
    except GameEvent.DoesNotExist:
        return render(request, 'game_event/game-event.html', {})
    player = Player.objects.get(user=request.user)
    if request.method == 'POST':
        text = request.POST.get('mytextbox', '')
        try:
            Message.create(player, event, text)
        except ValidationError as e:
            error_messages = e.messages[0].split("\n")
            for error in error_messages:
                messages.error(request, error)
    return redirect('game_event', id=id)
