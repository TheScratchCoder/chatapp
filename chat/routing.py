from django.urls import re_path
from . import consumers

# WebSocket URL patterns
# When browser connects to ws://localhost:8000/ws/chat/general/
# → it routes to ChatConsumer with room_slug = "general"

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_slug>[\w-]+)/$', consumers.ChatConsumer.as_asgi()),
]
