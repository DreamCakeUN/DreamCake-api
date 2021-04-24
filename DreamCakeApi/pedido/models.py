from django import forms
from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres import *
# Create your models here.

class Pastel(models.Model):
    usuarios = models.ManyToManyField(User)
    costo = models.FloatField(blank=True)
    status_pastel = models.BooleanField(blank=True)
    num_pisos = models.IntegerField(blank=True)
    porciones = models.IntegerField(blank=True)
    

class Pedido(models.Model):
    pasteles = models.ManyToManyField(Pastel)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=255)
    costo = models.FloatField(blank=True) 
    status = models.BooleanField(blank=True)
    correo_asociado = models.EmailField(max_length=255)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    comentario = models.CharField(max_length =255)
