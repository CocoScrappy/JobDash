"""
ASGI config for django_config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os
import django

django.setup()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_config.settings')
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
import job_posting.websocket.routing as routing



application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket":AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(routing.websocket_urlpatterns))
        )
    }
)

# channel_layer = channels.layers.get_channel_layer()