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
from users.views import photoViewList
from django.conf.urls import include
from social import views as social_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('stats/', include('statistics_api.urls')),
    path('users/', include('users.urls')),
    path('photos/', photoViewList.as_view(), name='photo_list'),
    path('social/', social_views.list_posts)
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
