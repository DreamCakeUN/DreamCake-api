from django.db import models

# Create your models here.
class Banner(models.Model):
    title = models.CharField(max_length = 100)
    text = models.TextField()
    abstract = models.CharField(max_length = 300)
    publication_date = models.DateTimeField(auto_now_add = True, null = True)
    image = models.ImageField(null = True, blank  = True)
    status = models.BooleanField()

    def __str__(self):
        return self.title