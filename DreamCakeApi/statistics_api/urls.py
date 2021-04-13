from django.urls import path
from . import views

urlpatterns = [
	path('users/', views.user_count),
	path('posts/', views.post_count),
	path('interactions/', views.inte_count)
]