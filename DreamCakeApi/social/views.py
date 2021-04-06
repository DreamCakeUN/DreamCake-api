from django.shortcuts import render
from social.models import Post
from django.http import HttpResponse, JsonResponse
from .serializers import PostSerializer
from django.db.models.functions import Coalesce
# Create your views here.



def list_posts(request):

    if request.method == 'GET':
        posts = Post.objects.all().order_by(Coalesce('likes','usuario').desc())[:3]
        serializer = PostSerializer(posts,many=True)
        return JsonResponse(serializer.data,safe=False) 