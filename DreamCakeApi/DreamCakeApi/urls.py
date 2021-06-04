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
from banner.views import photoViewList
from django.conf.urls import include
from social import views as social_views
from banner import views as banner_views
from pedido import views as pedido_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('stats/', include('statistics_api.urls')),
    path('users/', include('users.urls')),
    path('photos/', banner_views.photoViewList),
    path('social/', include('social.urls')),
    path('pasteles/', pedido_views.list_pasteles),
    path('pasteles/<int:pk>/', pedido_views.pasteles_details),
    path('pedidos/', pedido_views.list_pedidos),
    path('crear_pedido/', pedido_views.CrearPedido.as_view(), name='Crear Pedido'),
    path('crear_pastel/', pedido_views.CrearPastel.as_view(), name='Crear Pastel'),
    path('pedido/<int:id_pedido>/', pedido_views.list_pedidos_details),
    path('delpedido/<int:id_pedido>/', pedido_views.eliminar_pedido),
    path('modificar_pastel/<int:pk>/', pedido_views.ModificarPastel.as_view(), name='Modificar Pastel'),
    path('aceptar_pedido/<int:pk>/', pedido_views.AceptarPedido.as_view(), name='Aceptar Pedido'),
    path('estado_pedido/<int:pk>/', pedido_views.EstadoPedido.as_view(), name='Estado Pedido'),
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
