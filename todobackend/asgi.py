"""
ASGI config for todobackend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

# import os

# from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todobackend.settings')

# application = get_asgi_application()


import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todobackend.settings')

from django.core.asgi import get_asgi_application

# Initialize Django first
django_asgi_app = get_asgi_application()

#  Now it's safe to import Channels stuff
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import main.routing
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from main.utils import TokenAuthMiddleware


application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": TokenAuthMiddleware(
        URLRouter(
            main.routing.websocket_urlpatterns
        )
    ),
})