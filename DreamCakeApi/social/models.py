from django.db import models

from django.utils import timezone
# Create your models here.

from django.conf import settings
User = settings.AUTH_USER_MODEL


class Post(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    foto = models.ImageField(upload_to='postImages')
    likes = models.IntegerField(blank=True)
    status = models.BooleanField(blank=True)
    published_date = models.DateTimeField(auto_now_add=True)

    #def publish(self):
    #    self.save()    