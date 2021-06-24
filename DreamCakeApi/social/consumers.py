from django.contrib.sessions.models import Session

from users.models import User
from pedido.models import Pedido
from social.models import Post

from users.serializers import UserSerializer
from pedido import serializers as pedido_serializers
from social import serializers as social_serializers

from asgiref.sync import sync_to_async

from djangochannelsrestframework import permissions
from djangochannelsrestframework.observer import model_observer
from djangochannelsrestframework.decorators import action

from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    PatchModelMixin,
    UpdateModelMixin,
    CreateModelMixin,
    DeleteModelMixin,
)

# session_key = '8cae76c505f15432b48c8292a7dd0e54'


# session_data = session.get_decoded()
# print session_data
# uid = session_data.get('_auth_user_id')
# user = User.objects.get(id=uid)

class AdminAuthenticationPermission(permissions.BasePermission):
    async def has_permission(self, scope, consumer, action):
        cookies = scope.get("cookies")

        if 'sessionid' in cookies.keys():
            sessionid = cookies['sessionid']
            
            session = sync_to_async(Session.objects.get)(session_key=sessionid)

            session_data = (await session).get_decoded()
            uid = await sync_to_async(session_data.get)('_auth_user_id')
            user = await sync_to_async(User.objects.get)(id=uid)

            return user.is_superuser

        return False


class AuthenticationPermission(permissions.BasePermission):
    async def has_permission(self, scope, consumer, action):
        cookies = scope.get("cookies")

        if 'sessionid' in cookies.keys():
            sessionid = cookies['sessionid']
            
            session = sync_to_async(Session.objects.get)(session_key=sessionid)

            session_data = (await session).get_decoded()
            uid = await sync_to_async(session_data.get)('_auth_user_id')
            user = await sync_to_async(User.objects.get)(id=uid)

            return user.is_active

        return False

class PedidoConsumer(GenericAsyncAPIConsumer,):
    queryset = Pedido.objects.all()
    serializer_class = pedido_serializers.PedidoSerializer
    permission_classes = (AdminAuthenticationPermission,)

    @model_observer(Pedido)
    async def pedido_activity(self, message: pedido_serializers.PedidoSerializer, observer=None, **kwargs):
        await self.send_json(message.data)

    @pedido_activity.serializer
    def pedido_activity(self, instance: Pedido, action, **kwargs) -> pedido_serializers.PedidoSerializer:
        return pedido_serializers.PedidoSerializer(instance)

    @action()
    async def subscribe_to_pedido_activity(self, **kwargs):
        await self.pedido_activity.subscribe()

class PostConsumer(GenericAsyncAPIConsumer,):
    queryset = Post.objects.all()
    serializer_class = social_serializers.PostSerializer
    permission_classes = (AuthenticationPermission,)

    @model_observer(Post)
    async def post_activity(self, message: social_serializers.PostSerializer, observer=None, **kwargs):
        await self.send_json(message.data)

    @post_activity.serializer
    def post_activity(self, instance: Post, action, **kwargs) -> social_serializers.PostSerializer:
        return social_serializers.PostSerializer(instance)

    @action()
    async def subscribe_to_post_activity(self, **kwargs):
        await self.post_activity.subscribe()
