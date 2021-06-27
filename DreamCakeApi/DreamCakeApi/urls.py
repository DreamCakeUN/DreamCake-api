"""DreamCakeApi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
#from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include
from social import views as social_views
from banner import views as banner_views
from pedido import views as pedido_views

from django.urls import re_path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('stats/', include('statistics_api.urls')),
    path('users/', include('users.urls')),
    path('social/', include('social.urls')),
    path('pasteles/', pedido_views.GetCake.as_view(), name='Pasteles del usuerio actual'),
    path('pedidos/', pedido_views.GetUserPedidos.as_view(), name='Pedidos del usuerio actual'),
    path('pasteles/<user_email>/', pedido_views.GetUserCake.as_view(), name='pasteles del usuario con email'),
    path('pedidos/<user_email>/', pedido_views.ListPedidos.as_view(), name='pedidos usuario'),
    path('crear_pedido/', pedido_views.CrearPedido.as_view(), name='Crear Pedido'),
    path('crear_pastel/', pedido_views.CrearPastel.as_view(), name='Crear Pastel'),
    path('pedido/<int:id_pedido>/', pedido_views.list_pedidos_details),
    path('delpedido/<int:id_pedido>/', pedido_views.eliminar_pedido),
    path('modificar_pastel/<int:pk>/', pedido_views.ModificarPastel.as_view(), name='Modificar Pastel'),
    path('guardar_pastel/<int:pk>/', pedido_views.CopiarPasel.as_view(), name='Copiar Pastel'),
    path('copiar_pastel/<int:pk>/', pedido_views.EditarPastel.as_view(), name='Copiar Pastel'),
    path('aceptar_pedido/<int:pk>/', pedido_views.AceptarPedido.as_view(), name='Aceptar Pedido'),
    path('estado_pedido/<int:pk>/', pedido_views.EstadoPedido.as_view(), name='Estado Pedido'),
    path('all_pedidos/<atr>/', pedido_views.AllPedidos.as_view(), name='todos los pedidos'),
    path('pedido_by_status/<int:status>/<atr>/', pedido_views.PedidosByStatus.as_view(), name='pedidos con status'),
    path('pedido_by_accept/<int:acp>/<atr>/', pedido_views.PedidosByAccept.as_view(), name='Estado pedidos con accpt'),
    path('banner/get_all/', banner_views.GetAllBanners.as_view(), name='get all banners'),
    path('banner/create/', banner_views.CreateBanner.as_view(), name='create babber'),
    path('banner/delete/<int:pk>/', banner_views.EditStatusBanner.as_view(), name='update banner')
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
