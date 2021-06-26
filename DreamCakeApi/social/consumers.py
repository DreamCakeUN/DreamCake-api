from django.contrib.sessions.models import Session

from users.models import User
from pedido.models import Pedido
from social.models import Post, Comentario

from users.serializers import UserSerializer
from pedido import serializers as pedido_serializers
from social import serializers as social_serializers

# from asgiref.sync import sync_to_async

# from channels.db import database_sync_to_async

# from djangochannelsrestframework import permissions
# from djangochannelsrestframework.observer import model_observer
# from djangochannelsrestframework.decorators import action

# from djangochannelsrestframework.generics import GenericAsyncAPIConsumer, AsyncAPIConsumer
# from djangochannelsrestframework.mixins import (
#     ListModelMixin,
#     RetrieveModelMixin,
#     PatchModelMixin,
#     UpdateModelMixin,
#     CreateModelMixin,
#     DeleteModelMixin,
# )

from rest_live.mixins import RealtimeMixin
from rest_framework import generics
from rest_framework import permissions

from rest_framework import authentication


# session_key = '8cae76c505f15432b48c8292a7dd0e54'


# session_data = session.get_decoded()
# print session_data
# uid = session_data.get('_auth_user_id')
# user = User.objects.get(id=uid)

# class AdminAuthenticationPermission(permissions.BasePermission):
#     async def has_permission(self, scope, consumer, action):
#         cookies = scope.get("cookies")

#         if 'sessionid' in cookies.keys():
#             sessionid = cookies['sessionid']
            
#             session = sync_to_async(Session.objects.get)(session_key=sessionid)

#             session_data = (await session).get_decoded()
#             uid = await sync_to_async(session_data.get)('_auth_user_id')
#             user = await database_sync_to_async(User.objects.get)(id=uid)

#             return user.is_superuser

#         return False


# class AuthenticationPermission(permissions.BasePermission):
#     async def has_permission(self, scope, consumer, user_pk, action):
#         cookies = scope.get("cookies")

#         if 'sessionid' in cookies.keys():
#             # sessionid = cookies['sessionid']
            
#             # session = sync_to_async(Session.objects.get)(session_key=sessionid)

#             # session_data = (await session).get_decoded()
#             # uid = await sync_to_async(session_data.get)('_auth_user_id')
#             user = await database_sync_to_async(User.objects.get)(email=user_pk)

#             return user.is_active

#         return True

# class PedidoConsumer(GenericAsyncAPIConsumer,):
#     queryset = Pedido.objects.all()
#     serializer_class = pedido_serializers.PedidoSerializer
#     permission_classes = (AdminAuthenticationPermission,)

#     @model_observer(Pedido)
#     async def pedido_activity(self, message: pedido_serializers.PedidoSerializer, observer=None, **kwargs):
#         await self.send_json(message.data)

#     @pedido_activity.serializer
#     def pedido_activity(self, instance: Pedido, action, **kwargs) -> pedido_serializers.PedidoSerializer:
#         return pedido_serializers.PedidoSerializer(instance)

#     @action()
#     async def subscribe_to_pedido_activity(self, **kwargs):
#         await self.pedido_activity.subscribe()

# class PostConsumer(GenericAsyncAPIConsumer,):
#     queryset = Post.objects.all()
#     serializer_class = social_serializers.PostSerializer
#     permission_classes = (AuthenticationPermission,)

#     @model_observer(Post)
#     async def post_activity(self, message: social_serializers.PostSerializer, observer=None, **kwargs):
#         await self.send_json(message.data)

#     @post_activity.serializer
#     def post_activity(self, instance: Post, action, **kwargs) -> social_serializers.PostSerializer:
#         return social_serializers.PostSerializer(instance)

#     @action()
#     async def subscribe_to_post_activity(self, **kwargs):
#         await self.post_activity.subscribe()


# class PedidoUserConsumer(GenericAsyncAPIConsumer,):
#     queryset = Pedido.objects.all()
#     serializer_class = pedido_serializers.PedidoSerializer
#     permission_classes = (AuthenticationPermission,)

#     @model_observer(Pedido)
#     async def pedido_user_activity(self, message: pedido_serializers.PedidoSerializer, observer=None, **kwargs):
#         await self.send_json(message.data)

#     @pedido_user_activity.serializer
#     def pedido_user_activity(self, instance: Pedido, action, **kwargs) -> pedido_serializers.PedidoSerializer:
#         return pedido_serializers.PedidoSerializer(instance)

#     @pedido_user_activity.groups_for_signal
#     def pedido_user_activity(self, instance: Pedido, **kwargs):
#         yield f'-user__{instance.user}' 

#     @pedido_user_activity.groups_for_consumer
#     def pedido_user_activity(self, user=None, **kwargs):
#         yield f'-user__{user.email}'

#     @action()
#     async def subscribe_to_pedido_user_activity(self, user_pk, **kwargs):
#         user = await database_sync_to_async(User.objects.get)(email=user_pk)
#         await self.pedido_user_activity.subscribe(user = user)

# class PedidoConsumer1(GenericAsyncAPIConsumer,):

#     queryset = Pedido.objects.all()
#     serializer_class = pedido_serializers.PedidoSerializer
#     permission_classes = (AuthenticationPermission,)

#     @model_observer(Pedido)
#     async def pedido_activity(self, message: pedido_serializers.PedidoSerializer, observer=None, **kwargs):
#         await self.send_json(message.data)

#     @pedido_activity.serializer
#     def pedido_activity(self, instance: Pedido, action, **kwargs) -> pedido_serializers.PedidoSerializer:
#         return pedido_serializers.PedidoSerializer(instance)

#     @action()
#     async def subscribe_to_pedido_user_activity(self, **kwargs):
#         cookies = self.scope.get("cookies")
#         sessionid = cookies['sessionid']
            
#         session = sync_to_async(Session.objects.get)(session_key=sessionid)

#         session_data = (await session).get_decoded()
#         uid = await sync_to_async(session_data.get)('_auth_user_id')
#         user = await sync_to_async(User.objects.get)(id=uid)
        
#         await self.pedido_activity.subscribe(user = user)
#         # await self.pedido_activity.subscribe()

class AdminAuthenticationPermission(permissions.BasePermission):
    ADMIN_ONLY_AUTH_CLASSES = [authentication.BasicAuthentication, authentication.SessionAuthentication]

    def has_permission(self, request, view):
        user = request.user
        if user and user.is_superuser:
            return user.is_superuser or \
                not any(isinstance(request._authenticator, x) for x in self.ADMIN_ONLY_AUTH_CLASSES) 
        return False


class ModeratorAuthenticationPermission(permissions.BasePermission):
    ADMIN_ONLY_AUTH_CLASSES = [authentication.BasicAuthentication, authentication.SessionAuthentication]

    def has_permission(self, request, view):
        user = request.user
        if user and user.is_staff:
            return user.is_staff or \
                not any(isinstance(request._authenticator, x) for x in self.ADMIN_ONLY_AUTH_CLASSES) 
        return False

class PedidoUserConsumer(generics.ListAPIView, RealtimeMixin):
    serializer_class = pedido_serializers.PedidoSerializer
    queryset = Pedido.objects.all() 
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Pedido.objects.filter(user=self.request.user.email)

class PedidoConsumer(generics.ListAPIView, RealtimeMixin):
    serializer_class = pedido_serializers.PedidoSerializer
    queryset = Pedido.objects.all() 
    permission_classes = [permissions.IsAuthenticated, AdminAuthenticationPermission]

class PostConsumer(generics.ListAPIView, RealtimeMixin):
    serializer_class = social_serializers.PostSerializer
    queryset = Post.objects.all() 
    permission_classes = [permissions.IsAuthenticated]

class ComConsumer(generics.ListAPIView, RealtimeMixin):
    serializer_class = social_serializers.ComSerializer
    queryset = Comentario.objects.all() 
    permission_classes = [permissions.IsAuthenticated]

class PostUserConsumer(generics.ListAPIView, RealtimeMixin):
    serializer_class = social_serializers.PostSerializer
    queryset = Post.objects.all() 
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(usuario=self.request.user.email)