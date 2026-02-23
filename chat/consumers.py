import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import Room, Message


class ChatConsumer(AsyncWebsocketConsumer):
    """
    WebSocket Consumer — handles real-time messaging.

    How it works:
    1. User opens the chat page → browser connects via WebSocket
    2. connect()   → user joins a "channel group" (the room)
    3. receive()   → user sends a message → save to DB → broadcast to group
    4. disconnect()→ user leaves → removed from channel group

    All users in the same room_group receive messages in real time via Redis.
    """

    async def connect(self):
        """Called when a WebSocket connection is opened"""

        # Get room slug from the URL (e.g. /ws/chat/general/)
        self.room_slug = self.scope['url_route']['kwargs']['room_slug']

        # Create a unique group name for this room in Redis
        self.room_group_name = f'chat_{self.room_slug}'

        # Add this WebSocket connection to the room's group in Redis
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Accept the WebSocket connection
        await self.accept()

    async def disconnect(self, close_code):
        """Called when a WebSocket connection is closed"""

        # Remove this connection from the room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """Called when a message is received from the browser"""

        # Parse the incoming JSON message
        data = json.loads(text_data)
        message_content = data['message']
        username = self.scope['user'].username

        # Save the message to the database
        await self.save_message(username, self.room_slug, message_content)

        # Broadcast the message to ALL users in this room group (via Redis)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',          # maps to the method below
                'message': message_content,
                'username': username,
            }
        )

    async def chat_message(self, event):
        """Called when a message is broadcast to the group — sends it to browser"""

        # Send the message back to the WebSocket (browser)
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'username': event['username'],
        }))

    @database_sync_to_async
    def save_message(self, username, room_slug, content):
        """Save message to database (sync DB operation wrapped for async)"""
        user = User.objects.get(username=username)
        room = Room.objects.get(slug=room_slug)
        Message.objects.create(room=room, author=user, content=content)
