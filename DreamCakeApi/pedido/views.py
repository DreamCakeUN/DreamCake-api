from django.shortcuts import render
from pedido.models import Pastel, Pedido
from django.http import HttpResponse, JsonResponse
from .serializers import PastelSerializer, PedidoSerializer
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

@api_view(['GET','POST'])

def list_pasteles(request):
    if request.method == 'GET':
        pasteles = Pastel.objects.all()
        serializer = PastelSerializer(pasteles,many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
         serializer = PastelSerializer(data = request.data)
         if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

@api_view(['GET','PUT','DELETE'])

def pasteles_details(request,pk):
    try:
        pastel = Pastel.objects.get(pk=pk)
    except Pastel.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PastelSerializer(pastel)
        return Response(serializer.data)

    elif request.method == 'PUT':
         serializer = PastelSerializer(pastel, data = request.data)
         if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)          
    
    elif request.method == 'DELETE':
        pastel.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

def list_pedidos(request):

    if request.method == 'GET':
        posts = Pedido.objects.all()
        serializer = PedidoSerializer(posts,many=True)
        return JsonResponse(serializer.data,safe=False)   

@api_view(['GET','POST'])

def mod_pedido_get(request, id_pedido):
    if request.method == 'GET':
        pedido = Pedido.objects.filter(id = id_pedido)
        serializer = PedidoSerializer(pedido,many=True)
        return JsonResponse(serializer.data,safe=False)   

"""def mod_pedido_post(request, id_pedido):
    if request.method == 'POST':"""
