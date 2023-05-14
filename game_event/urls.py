from django.urls import path
from . import views


urlpatterns = [
    path('create/', views.display_game_event_form, name='display game event form'),
    path('create/process', views.process_game_event_form, name='process game event form'),
    path('', views.game_events, name='game-events'),
    path('<id>/', views.game_event, name='game_event'),
    path('join-event/<id>/', views.join_event, name='join_event'),
    path('process-answer-game-event/<id>/', views.process_answer_game_event, name='process_answer_game_event'),
    path('remove-from-event/<id>/', views.remove_from_event, name='remove_from_event')]
