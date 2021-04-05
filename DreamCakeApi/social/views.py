from django.shortcuts import render
from social.models import Post
from django.http import HttpResponse
# Create your views here.



def list_posts(request):
    posts = Post.objects.all()
    return render(request, 'posts/posts.html',{'posts': posts})