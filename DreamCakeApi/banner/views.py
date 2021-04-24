from django.shortcuts import render
from banner.models import Banner
from django.http import HttpResponse, JsonResponse
from .serializers import BannerSerializer
# Create your views here.

def photoViewList(request):

    if request.method == 'GET':
        promos = Banner.objects.all()
        serializer = BannerSerializer(promos,many=True)
        return JsonResponse(serializer.data,safe=False) 