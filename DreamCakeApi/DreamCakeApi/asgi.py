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
# import social.routing
from social import consumers

from django.urls import path

from rest_live.routers import RealtimeRouter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DreamCakeApi.settings')


pedidoUserRouter = RealtimeRouter()
pedidoUserRouter.register(consumers.PedidoUserConsumer)

pedidoAdminRouter = RealtimeRouter()
pedidoAdminRouter.register(consumers.PedidoConsumer)

socialGeneralRouter = RealtimeRouter()
socialGeneralRouter.register(consumers.PostConsumer)
socialGeneralRouter.register(consumers.ComConsumer)

UserSocialRouter = RealtimeRouter()
UserSocialRouter.register(consumers.PostUserConsumer)


application = ProtocolTypeRouter({
    # "http": get_asgi_application(),
	"websocket": AuthMiddlewareStack(
        URLRouter([
            path("ws/pedidoUser/", pedidoUserRouter.as_consumer(), name="subscriptions pedido"),
            path("ws/pedido/", pedidoAdminRouter.as_consumer(), name="subscriptions admin pedido"),
            path("ws/socialGeneral/", socialGeneralRouter.as_consumer(), name='subscriptions social'),
            path("ws/socialUser/", UserSocialRouter.as_consumer(), name='subscriptions social user'),
        ])
    ),
    # Just HTTP for now. (We can add other protocols later.)
})


# application = get_asgi_application()


