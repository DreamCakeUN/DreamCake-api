from django.shortcuts import render
from social.models import Post, Comentario
from django.http import HttpResponse, JsonResponse
from .serializers import PostSerializer
from django.db.models.functions import Coalesce

from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
# Create your views here.

from . import serializers

def list_posts(request):

    if request.method == 'GET':
        posts = Post.objects.all().order_by(Coalesce('likes','usuario').desc())[:3]
        serializer = PostSerializer(posts,many=True)
        return JsonResponse(serializer.data,safe=False) 

class getAllPosts(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    lookup_url_kwarg = "atr"

    def get_queryset(self):
        atr = self.kwargs.get(self.lookup_url_kwarg)
        return Post.objects.filter(status = True).order_by(atr)

class getAllCom(generics.ListAPIView):
    queryset = Comentario.objects.all()
    serializer_class =serializers.ComSerializer
    lookuo_url_kwarg = 'post'

    def get_queryset(self):
        post = self.kwargs.get(self.lookup_url_kwarg)
        return Comentario.objects.filter(post = post).order_by('fecha')

class createPost(generics.CreateAPIView):
    serializer_class = serializers.PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({
            'status': 200,
            'message': 'Post creado',
            'data': response.data
        })

class createCom(generics.CreateAPIView):
    serializer_class = serializers.ComSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({
            'status': 200,
            'message': 'Com creado',
            'data': response.data
        })

