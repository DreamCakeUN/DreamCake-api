from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth.models import User

# Conteo de usuarios
def user_count(request):
	return HttpResponse(User.objects.all().count())

# Conteo de posts
def post_count(request):
	# return HttpResponse(User.objects.all().count())
	return HttpResponse('POSTS')

# Conteo de comentarios
def inte_count(request):
	# return HttpResponse(User.objects.all().count())
	return HttpResponse('COMENTARIOS + LIKES + ...')