from django.shortcuts import render
from banner.models import Banner
from django.http import HttpResponse, JsonResponse
from .serializers import BannerSerializer, BannerSerializerEdit

from rest_framework import generics
from rest_framework import permissions
from rest_framework import authentication
# Create your views here.

# def photoViewList(request):

#     if request.method == 'GET':
#         promos = Banner.objects.all()
#         serializer = BannerSerializer(promos,many=True)
#         return JsonResponse(serializer.data,safe=False) 
class AdminAuthenticationPermission(permissions.BasePermission):
    ADMIN_ONLY_AUTH_CLASSES = [authentication.BasicAuthentication, authentication.SessionAuthentication]

    def has_permission(self, request, view):
        user = request.user
        if user and user.is_superuser:
            return user.is_superuser or \
                not any(isinstance(request._authenticator, x) for x in self.ADMIN_ONLY_AUTH_CLASSES) 
        return False

class GetAllBanners(generics.ListAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
    permission_classes = [permissions.AllowAny]

class CreateBanner(generics.CreateAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
    permission_classes = [AdminAuthenticationPermission]

class EditStatusBanner(generics.UpdateAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializerEdit
    permission_classes = [AdminAuthenticationPermission]
    lookup_url_kwarg = 'pk'