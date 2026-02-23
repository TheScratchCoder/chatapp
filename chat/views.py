from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.utils.text import slugify
from .models import Room, Message
from .forms import RegisterForm, RoomForm


def register(request):
    """User registration view"""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)           # auto-login after register
            return redirect('room_list')
    else:
        form = RegisterForm()
    return render(request, 'chat/register.html', {'form': form})


@login_required
def room_list(request):
    """Home page — shows all available chat rooms"""
    rooms = Room.objects.all().order_by('-created_at')
    return render(request, 'chat/room_list.html', {'rooms': rooms})


@login_required
def create_room(request):
    """Create a new chat room"""
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.slug = slugify(room.name)     # "Tech Talk" → "tech-talk"
            room.created_by = request.user
            room.save()
            return redirect('room_detail', room_slug=room.slug)
    else:
        form = RoomForm()
    return render(request, 'chat/create_room.html', {'form': form})


@login_required
def room_detail(request, room_slug):
    """
    The actual chat room page.
    - Loads the room + last 20 messages from DB
    - The page then opens a WebSocket connection for real-time messaging
    """
    room = get_object_or_404(Room, slug=room_slug)
    chat_messages = room.get_last_20_messages()
    return render(request, 'chat/room_detail.html', {
    'room': room,
    'chat_messages': chat_messages,
})
