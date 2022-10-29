from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from . import models
from . import forms
from base.models import Topic, Message


def user_profile(request, pk):
    user = models.User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.filter(user=user)
    topics = Topic.objects.all()

    context = {
        'user': user,
        'rooms': rooms,
        'topics': topics,
        'room_messages': room_messages,
    }
    return render(request, 'users/user_profile.html', context)


@login_required(login_url='login')
def user_profile_edit(request, pk):
    user = models.User.objects.get(id=pk)
    
    if request.method == 'POST':
        form = forms.UserProfileUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', pk=user.id)
    
    form = forms.UserProfileUpdateForm(instance=user)
    context = {
        'form': form,
    }
    return render(request, 'users/user_profile_edit.html', context)


def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            user = None
            messages.error(request, 'User does not exist!')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password is incorrect!')

    context = {
        
    }
    return render(request, 'users/login.html', context)


def user_registration(request):

    if request.method == 'POST':
        form = forms.UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('login')
        else:
            messages.error(request, 'An error occurred during registration!')

    form = forms.UserRegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'users/registration.html', context)


def user_logout(request):
    logout(request)
    messages.info(request, 'Logged out!')
    return redirect('login')


def activity_page(request):
    room_messages = Message.objects.all()
    
    context = {
        'room_messages': room_messages,
    }
    return render(request, 'users/activity.html', context)

