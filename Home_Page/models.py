from django.db import models
from django.urls import reverse


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=SmartHun.Status.PUBLISHED)


class SmartHun(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Чорновик'
        PUBLISHED = 1, 'Опубліковано'

    name = models.CharField(max_length=50)
    content = models.TextField(blank=True, null=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
                                       default=Status.DRAFT)
    photo = models.ImageField(upload_to='photo/%Y/%m/%d/', default=None, blank=True, null=True)
    objects = models.Manager()
    published = PublishedManager()


    def __str__(self):
        return self.name


class Notebooks(models.Model):
    name = models.CharField(max_length=50)
    content = models.TextField(null=True)
    rating = models.TextField(blank=True, null=True)
    price = models.TextField(blank=True, null=True)
    url_name = models.URLField()
    images = models.ImageField(null=True, max_length=200)
    Notebooks_brand = models.ManyToManyField('NotebooksBrand', blank=True)
    
    
class Laptop_images(models.Model):
    images_id = models.ForeignKey(Notebooks, related_name='images_id', on_delete=models.CASCADE)
    image_path = models.CharField(max_length=255)


class NotebooksBrand(models.Model):
    name = models.CharField(max_length=20)
    url_name = models.URLField()

