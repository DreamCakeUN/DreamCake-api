from django.shortcuts import render
from pedido.models import Pastel, Pedido
from django.http import HttpResponse, JsonResponse
from .serializers import PastelSerializer, PedidoSerializer
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
@csrf_exempt
def list_pasteles(request):

    if request.method == 'GET':
        posts = Pastel.objects.all()
        serializer = PastelSerializer(posts,many=True)
        return JsonResponse(serializer.data,safe=False)
    elif request.method == 'POST':
         data = JSONParser.parse(request)
         serializer = PastelSerializer(data = data)
         if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data,status=201)
         return JsonResponse(serializer.errors, status=400)



def list_pedidos(request):

    if request.method == 'GET':
        posts = Pedido.objects.all()
        serializer = PedidoSerializer(posts,many=True)
        return JsonResponse(serializer.data,safe=False)         