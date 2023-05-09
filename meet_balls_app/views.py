from django.shortcuts import render
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages


def home(request):
    return render(request, 'meet_balls_app/home.html')


def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'meet_balls_app/home.html',
                          {'user': {'is_authenticated': True, 'username': username}})
        else:
            error_message = "Invalid username or password."
            messages.error(request, error_message)
            return render(request, 'meet_balls_app/login.html', {'user': {'is_authenticated': False, 'username': None}})
    else:
        return render(request, 'meet_balls_app/login.html', {'user': {'is_authenticated': False, 'username': None}})


def logoutUser(request):
    logout(request)
    return render(request, 'meet_balls_app/home.html', {'user': {'is_authenticated': False}})
