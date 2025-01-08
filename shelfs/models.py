from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Shelf(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField(default='')
    image = models.ImageField(default='shelf.png')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
class Item(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField(default='')
    image = models.ImageField(default='https://static.thenounproject.com/png/4241034-200.png')
    quantity = models.PositiveIntegerField(default=1)
    date = models.DateTimeField(default=timezone.now)
    shelf = models.ForeignKey(Shelf, on_delete=models.CASCADE)

    def __str__(self):
        return self.title