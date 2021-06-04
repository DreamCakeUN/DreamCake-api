from django.urls import include, path, re_path
from . import views

urlpatterns = [
	path(
        'all_posts/<atr>',
        views.getAllPosts.as_view(),
        name='get all posts'
    ),
	path(
        'create_post/',
        views.createPost.as_view(),
        name='create post'
    ),
	path(
        'create_com/',
        views.createCom.as_view(),
        name='crear comentario'
    ),
]