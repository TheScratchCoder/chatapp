"""
ASGI config for chatproject.

This is the KEY file that makes real-time possible.
- Django normally uses WSGI (synchronous, HTTP only)
- ASGI supports both HTTP and WebSocket (async)
- Django Channels uses this to handle WebSocket connections
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chat.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatproject.settings')

application = ProtocolTypeRouter({
    # Regular HTTP requests go to Django as normal
    'http': get_asgi_application(),

    # WebSocket requests go through AuthMiddleware → URLRouter → our Consumer
    'websocket': AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})
