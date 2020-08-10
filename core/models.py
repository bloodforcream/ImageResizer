from django.db import models


class Image(models.Model):
    image = models.ImageField(upload_to='images')
    slug = models.SlugField(max_length=40)
