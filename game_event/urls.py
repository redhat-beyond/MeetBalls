from django.urls import path
from . import views


urlpatterns = [
    path('create/', views.display_game_event_form, name='display game event form'),
    path('create/process', views.process_game_event_form, name='process game event form'),
    ]
