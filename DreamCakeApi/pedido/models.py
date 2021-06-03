from django import forms
from django.db import models

from django.contrib.postgres import *
from django.utils.translation import gettext_lazy as _
# Create your models here.

from django.conf import settings
User = settings.AUTH_USER_MODEL

class Pastel(models.Model):
    usuarios = models.ManyToManyField(User, related_name= "pasteles")
    
    status_pastel = models.BooleanField(blank=True)
    
    class Formas(models.TextChoices):
        Circular = 'CI', _('Circular')
        Cuadrado = 'CU', _('Cuadrado')

    forma = models.TextField(choices=Formas.choices)

    num_pisos = models.IntegerField(blank=True)
    
    porciones = models.IntegerField(blank=True)

    class Masas(models.TextChoices):
        Vainilla = 'VA', _('Vainilla')
        Chocolate = 'CH', _('Chocolate')
        Tres_Leches = 'TL', _('Tres Leches')
        Red_Velvet = 'RV', _('RedVelvet')

    masa = models.CharField(
        choices=Masas.choices,
        max_length=2
    )

    class Rellenos(models.TextChoices):
        Arequipe = 'AQ', _('Arequipe')
        Nutella = 'NU', _('Nutella')
        Mermelada = 'ML', _('Mermelada') 
        Crema_Pastelera = 'CP', _('CremaPastelera')

    relleno = models.CharField(
        choices=Rellenos.choices,
        max_length=2
    )

    class Cobertura(models.TextChoices):
        Crema = 'CR', _('Crema')
        Fondant = 'FD', _('Fondant')

    Cobertura = models.CharField(
        choices=Cobertura.choices,
        max_length=2
    )
    class ColorCobertura(models.TextChoices):
        Azul = 'AZ', _('Azul')
        Amarillo = 'AM', _('Amarillo')
        Blanco = 'BL', _('Amarillo')
        Verde = 'VD', _('Verde')
        Rojo = 'RJ', _('Rojo')

    ColorCobertura = models.CharField(
        choices=ColorCobertura.choices,
        max_length=2
    )

    costo = models.FloatField(blank=True, default=0)

    def __str__(self):
        return 'Pastel ' + str(self.id)
    

class Pedido(models.Model):
    pasteles = models.ForeignKey(Pastel, on_delete=models.CASCADE, null=True, related_name="pedidos", to_field="id")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="pedidos", to_field="email")
    
    direccion = models.CharField(max_length=255, null=True)
    costo = models.FloatField(blank=True) 
<<<<<<< HEAD
    status = models.BooleanField(blank=True)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    comentario = models.CharField(max_length =255)
    domiciliario = models.BooleanField(default=False)

    @property
    def userEmail(self):
        return self.user.email
=======
    status = models.IntegerField(blank=True)
    correo_asociado = models.EmailField(max_length=255)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    comentario = models.CharField(max_length =255)

class Imagen(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length = 180)
    upload_date = models.DateTimeField(auto_now_add = True, null = True)
    image = models.ImageField(upload_to='pedido', null = True, blank  = True)
>>>>>>> CAKE-49_ME_Pedido_BE
