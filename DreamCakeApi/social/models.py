from django.db import models

from django.utils import timezone
# Create your models here.

from django.conf import settings
User = settings.AUTH_USER_MODEL


class Post(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name="posts", to_field="email")
    foto = models.ImageField(upload_to='postImages')
    likes = models.IntegerField(default=0)
    reported = models.BooleanField(default=False)
    status = models.BooleanField(default=True)
    published_date = models.DateTimeField(auto_now_add=True)

    @property
    def userEmail(self):
        return self.user.email

    #def publish(self):
    #    self.save() 
    # 

class Comentario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name="comentarios", to_field="email")
    comentario = models.CharField(max_length=250)
    fecha = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False, related_name="comentarios", to_field="id")
