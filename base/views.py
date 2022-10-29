from django.shortcuts import redirect, render
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from . import models
from . import forms


def home(request):
    q = request.GET.get('q') if request.GET.get('q') else ''
    rooms = models.Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    rooms_total = rooms.count()
    topics = models.Topic.objects.all()
    room_messages = models.Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {
        'rooms': rooms,
        'topics': topics,
        'rooms_total': rooms_total,
        'room_messages': room_messages,
    }
    return render(request, 'base/index.html', context)


def single_room(request, pk):
    room = models.Room.objects.get(id=pk)
    comments = room.message_set.all()

    if request.method == 'POST':
        comment = models.Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('message')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {
        'room': room,
        'comments': comments,
        'participants': room.participants.all(),
    }
    return render(request, 'base/room.html', context)


@login_required(login_url='login')
def create_room(request):
    form = forms.RoomForm()
    topics = models.Topic.objects.all()

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = models.Topic.objects.get_or_create(name=topic_name)

        room = models.Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )
        return redirect('room', pk=room.id)

    context = {
        'form': form,
        'topics': topics,
        'text': 'Create',
    }
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def update_room(request, pk):
    user = models.User.objects.get(id=request.user.id)
    room = user.room_set.get(id=pk)
    form = forms.RoomForm(instance=room)
    topics = models.Topic.objects.all()

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = models.Topic.objects.get_or_create(name=topic_name)

        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()

        return redirect('home')

    context = {
        'form': form,
        'topics': topics,
        'text': 'Update',
        'room': room,
    }
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def delete_room(request, pk):
    user = models.User.objects.get(id=request.user.id)
    room = user.room_set.get(id=pk)

    if request.method == 'POST':
        room.delete()
        return redirect('home')

    context = {
        'obj': room,
    }
    return render(request, 'delete.html', context)


@login_required(login_url='login')
def delete_comment(request, pk):
    user = models.User.objects.get(id=request.user.id)
    comment = user.message_set.get(id=pk)
    next_url = request.GET.get('next') if request.GET.get('next') else None

    if request.method == 'POST':
        comment.delete()
        return redirect('room', pk=comment.room.id) if not next_url else redirect(next_url)
    context = {
        'obj': comment.body,
    }
    return render(request, 'delete.html', context)



def topics_page(request):
    q = request.GET.get('q') if request.GET.get('q') else ''
    topics = models.Topic.objects.filter(name__icontains=q)
    context = {
        'topics': topics,
    }
    return render(request, 'base/topics.html', context)

