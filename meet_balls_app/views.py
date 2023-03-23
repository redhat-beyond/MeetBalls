from django.shortcuts import render


def home(request):
    return render(request, 'meet_balls_app/home.html')
