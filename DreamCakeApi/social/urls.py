from django.urls import include, path, re_path
from . import views

urlpatterns = [
	path(
        'all_posts/<atr>/<int:count>',
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
	path(
		'comments/<int:post>',
		views.getAllCom.as_view(),
		name='comentarios del post'
	),
	path(
		'mod_com/<int:pk>',
		views.ModerateCom.as_view(),
		name='moderar post'
	),
	path(
		'mod_post/<int:pk>',
		views.ModeratePost.as_view(),
		name='moderar comentario'
	),
	path(
		'post_cake/<int:post>',
		views.getPostCake.as_view(),
		name='get cake from post'
	),
	path(
		'like/<int:pk>/', 
		views.LikePost.as_view(), 
		name='like post'
	),
]