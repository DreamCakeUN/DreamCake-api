from django import forms
from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres import *
from django.utils.translation import gettext_lazy as _
# Create your models here.

class Pastel(models.Model):
    usuarios = models.ManyToManyField(User)
    costo = models.FloatField(blank=True)
    status_pastel = models.BooleanField(blank=True)
    class Pisos(models.IntegerChoices):
        SENCILLO_1 = 1
        DOBLE_2 = 2
        TRIPLE_3 = 3
        ESPECIAL_4 = 4

    num_pisos = models.IntegerField(choices=Pisos.choices)
    class Porciones(models.IntegerChoices):
        _10 = 10
        _15 = 15
        _20 = 20
        _30 = 30
        
    porciones = models.IntegerField(choices=Porciones.choices)

    class Relleno(models.TextChoices):
        Vainilla = 'VA', _('Vainilla')
        Chocolate = 'CH', _('Chocolate')
        Merengue_Suizo = 'MS', _('MerengueSuizo')
        Crema_Queso = 'CQ', _('CremaQueso')
        Crema_Pastelera = 'CP', _('CremaPastelera')

    relleno = models.CharField(
        choices=Relleno.choices,
        max_length=2
    )

    class Cobertura(models.TextChoices):
        Azucar = 'AZ', _('Azucar')
        Mantequilla = 'MA', _('Mantequilla')
        Chocolate = 'CH', _('Chocolate')
        Chocolate_Blanco = 'CB', _('ChocolateBlanco')
        Fondant = 'FD', _('Fondant')

    Cobertrura = models.CharField(
        choices=Cobertura.choices,
        max_length=2
    )
    

class Pedido(models.Model):
    pasteles = models.ManyToManyField(Pastel)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=255)
    costo = models.FloatField(blank=True) 
    status = models.BooleanField(blank=True)
    correo_asociado = models.EmailField(max_length=255)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    comentario = models.CharField(max_length =255)
