from django.shortcuts import render
from social.models import Post, Comentario
from django.http import HttpResponse, JsonResponse
from .serializers import PostSerializer
from django.db.models.functions import Coalesce

from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import authentication
from rest_framework import status
from rest_framework import permissions
# Create your views here.

from . import serializers
from pedido.models import Pastel
from pedido.serializers import PastelSerializer


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



def list_posts(request):

    if request.method == 'GET':
        posts = Post.objects.all().order_by(Coalesce('likes','usuario').desc())[:3]
        serializer = PostSerializer(posts,many=True)
        return JsonResponse(serializer.data,safe=False) 

class getAllPosts(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    lookup_url_kwarg = "atr"
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        atr = self.kwargs.get(self.lookup_url_kwarg)
        count = self.kwargs.get("count")
        return Post.objects.filter(status = True).order_by(atr)[:count]

class getAllCom(generics.ListAPIView):
    queryset = Comentario.objects.all()
    serializer_class =serializers.ComSerializer
    lookup_url_kwarg = 'post'
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        post = self.kwargs.get(self.lookup_url_kwarg)
        return Comentario.objects.filter(post = post, status = True).order_by('fecha')

class getPostCake(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PastelSerializer
    lookup_url_kwarg = 'post'

    def get_object(self):
        post = self.kwargs.get(self.lookup_url_kwarg)
        cake = Post.objects.get(id = post).pastel
        return Pastel.objects.get(id = cake.id)

class createPost(generics.CreateAPIView):
    serializer_class = serializers.PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return response

class createCom(generics.CreateAPIView):
    serializer_class = serializers.ComSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return response

class ModerateCom(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated, AdminAuthenticationPermission or ModeratorAuthenticationPermission)
    serializer_class = serializers.ModCom

    lookup_url_kwarg = 'pk'
    queryset = Comentario.objects.all()

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_object())
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_object(), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
class ModeratePost(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated, AdminAuthenticationPermission or ModeratorAuthenticationPermission)
    serializer_class = serializers.ModPost

    lookup_url_kwarg = 'pk'
    queryset = Post.objects.all()

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_object())
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_object(), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
