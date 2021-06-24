"""
ASGI config for DreamCakeApi project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import social.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DreamCakeApi.settings')


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
	"websocket": AuthMiddlewareStack(
        URLRouter(
            social.routing.websocket_urlpatterns
        )
    ),
    # Just HTTP for now. (We can add other protocols later.)
})


# application = get_asgi_application()
