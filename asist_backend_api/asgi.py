import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "asist.settings")

import django
from django.urls import path
from django.conf import settings

if not settings.configured:
    django.setup()

from .middleware import TokenAuthMiddleware
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from searching import consumers as searching_consumers

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": TokenAuthMiddleware(
        URLRouter([
            path('ws/searching/progress/<str:token>/', searching_consumers.SearchProgressConsumer.as_asgi()),
        ])
    ),
})
