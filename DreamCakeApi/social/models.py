from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.


class Post(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    foto = models.CharField(max_length=255, blank=True)
    likes = models.IntegerField(blank=True)
    status = models.BooleanField(blank=True)
    published_date = models.DateTimeField(auto_now_add=True)

    def publish(self):
        self.save()
    
    