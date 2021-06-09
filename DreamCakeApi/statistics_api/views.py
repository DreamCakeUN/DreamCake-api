from django.shortcuts import render
from django.http import HttpResponse

from users.models import User
from social.models import Post
from social.models import Comentario

# Conteo de usuarios
def user_count(request):
	return HttpResponse(User.objects.filter(is_active = True).count())

# Conteo de posts
def post_count(request):
	return HttpResponse(Post.objects.filter(status = True).count())

# Conteo de comentarios
def inte_count(request):
	comentarios = Comentario.objects.all().count()
	likes = sum(p.likes for p in Post.objects.filter(status = True))

	return HttpResponse(comentarios + likes)
