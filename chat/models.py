from django.db import models
from django.contrib.auth.models import User


class Room(models.Model):
    """
    A chat room that multiple users can join.
    name       - display name e.g. "General", "Tech Talk"
    slug       - URL-friendly name e.g. "general", "tech-talk"
    created_by - the user who created the room
    created_at - timestamp
    """
    name       = models.CharField(max_length=100, unique=True)
    slug       = models.SlugField(max_length=100, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rooms_created')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_last_20_messages(self):
        """Return last 20 messages for this room (used to show history on join)"""
        return self.messages.order_by('-timestamp')[:20][::-1]


class Message(models.Model):
    """
    A single chat message.
    room      - which room this message belongs to
    author    - the user who sent it
    content   - the actual message text
    timestamp - when it was sent
    """
    room      = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages')
    author    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    content   = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author.username} in {self.room.name}: {self.content[:50]}'

    class Meta:
        ordering = ['timestamp']
