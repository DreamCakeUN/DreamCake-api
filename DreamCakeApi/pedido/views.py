from django.shortcuts import render
from pedido.models import Pastel, Pedido
from django.http import HttpResponse, JsonResponse
from .serializers import PastelSerializer, PedidoSerializer, AceptarPedido, EstadoPedido, AddUserToPaselSerializer, EditarPastelSerializer
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status

from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from rest_framework import authentication
from rest_framework import permissions

from users.models import User
# @api_view(['GET','POST'])

class AdminAuthenticationPermission(permissions.BasePermission):
    ADMIN_ONLY_AUTH_CLASSES = [authentication.BasicAuthentication, authentication.SessionAuthentication]

    def has_permission(self, request, view):
        user = request.user
        if user and user.is_superuser:
            return user.is_superuser or \
                not any(isinstance(request._authenticator, x) for x in self.ADMIN_ONLY_AUTH_CLASSES) 
        return False


class ModeratorAuthenticationPermission(permissions.BasePermission):
    ADMIN_ONLY_AUTH_CLASSES = [authentication.BasicAuthentication, authentication.SessionAuthentication]

    def has_permission(self, request, view):
        user = request.user
        if user and user.is_staff:
            return user.is_staff or \
                not any(isinstance(request._authenticator, x) for x in self.ADMIN_ONLY_AUTH_CLASSES) 
        return False

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



class CrearPedido(generics.CreateAPIView):
    serializer_class = PedidoSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return response

class CrearPastel(generics.CreateAPIView):
    serializer_class = PastelSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return response  

class EditarPastel(generics.CreateAPIView):
    serializer_class = EditarPastelSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def get_serializer_context(self):
        pk = self.kwargs.get(self.lookup_field)
        context = super().get_serializer_context()
        context["prev"] = Pastel.objects.filter(pk = pk).get()
        return context

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return response

class CopiarPasel(generics.RetrieveUpdateAPIView):
    queryset = Pastel.objects.all()
    lookup_field = 'pk'

    serializer_class = AddUserToPaselSerializer
    permission_classes = [IsAuthenticated]
 

def list_pedidos_details(request, id_pedido):
    if request.method == 'GET':
        pedido = Pedido.objects.filter(id = id_pedido)
        serializer = PedidoSerializer(pedido,many=True)
        return JsonResponse(serializer.data,safe=False)   

def mod_pedido_put(request, id_pedido):
    try:
        pedido = Pedido.objects.filter(id = id_pedido)
    except Pedido.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        serializer = PedidoSerializer(pedido, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

def eliminar_pedido(request, id_pedido):
    try:
        pedido = Pedido.objects.get(id = id_pedido)
    except Pedido.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':#?????
        pedido.status = 3
        pedido.save()
        return HttpResponse(request)

class ModificarPastel(generics.RetrieveUpdateAPIView):
    queryset = Pastel.objects.all()
    lookup_field = 'pk'

    serializer_class = PastelSerializer
    permission_classes = [IsAuthenticated, AdminAuthenticationPermission or ModeratorAuthenticationPermission]

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_object())
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_object(), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

class AceptarPedido(generics.RetrieveUpdateAPIView):
    queryset = Pedido.objects.all()
    lookup_field = 'pk'

    serializer_class = AceptarPedido
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_object())
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

class EstadoPedido(generics.RetrieveUpdateAPIView):
    queryset = Pedido.objects.all()
    lookup_field = 'pk'

    serializer_class = EstadoPedido
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_object())
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

class GetCake(generics.ListAPIView):
    queryset = Pastel.objects.all()
    
    serializer_class = PastelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Pastel.objects.filter(usuarios = self.request.user)

class GetUserCake(generics.ListAPIView):
    queryset = Pastel.objects.all()
    
    serializer_class = PastelSerializer
    permission_classes = [IsAuthenticated]

    lookup_url_kwarg = 'user_email'

    def get_queryset(self):
        useremail = self.kwargs.get(self.lookup_url_kwarg)
        user = User.objects.get(email = useremail)
        return Pastel.objects.filter(usuarios = user)


class ListPedidos(generics.ListAPIView):
    queryset = Pedido.objects.all()

    serializer_class = PedidoSerializer
    permission_classes = (permissions.IsAuthenticated, AdminAuthenticationPermission)

    lookup_url_kwarg = 'user_email'

    def get_queryset(self):
        userMail = self.kwargs.get(self.lookup_url_kwarg)
        # user = User.objects.get(pk = userMail)
        return Pedido.objects.filter(user = userMail)

class AllPedidos(generics.ListAPIView):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    lookup_url_kwarg = "atr"
    permission_classes = [AdminAuthenticationPermission]

    def get_queryset(self):
        atr = self.kwargs.get(self.lookup_url_kwarg)
        return Pedido.objects.all().order_by(atr)


class PedidosByStatus(generics.ListAPIView):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    lookup_url_kwarg = "status"
    permission_classes = [AdminAuthenticationPermission]

    def get_queryset(self):
        status = self.kwargs.get(self.lookup_url_kwarg)
        atr = self.kwargs.get("atr")
        return Pedido.objects.filter(estado = status).order_by(atr)

class PedidosByAccept(generics.ListAPIView):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    lookup_url_kwarg = "acp"
    permission_classes = [AdminAuthenticationPermission]

    def get_queryset(self):
        acp = self.kwargs.get(self.lookup_url_kwarg)
        atr = self.kwargs.get("atr")
        return Pedido.objects.filter(aceptado = acp).order_by(atr)