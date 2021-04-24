from django.shortcuts import render
from pedido.models import Pastel, Pedido
from django.http import HttpResponse, JsonResponse
from .serializers import PastelSerializer, PedidoSerializer
# Create your views here.

def list_pasteles(request):

    if request.method == 'GET':
        posts = Pastel.objects.all()
        serializer = PastelSerializer(posts,many=True)
        return JsonResponse(serializer.data,safe=False) 

def list_pedidos(request):

    if request.method == 'GET':
        posts = Pedido.objects.all()
        serializer = PedidoSerializer(posts,many=True)
        return JsonResponse(serializer.data,safe=False)         