from django.db import models

# Create your models here.

class Banner(models.Model):
    image = models.ImageField(upload_to='banners')
    index = models.IntegerField(unique=True)
    headline=models.TextField(blank=True, null=True)
    description=models.TextField(blank=True, null=True)