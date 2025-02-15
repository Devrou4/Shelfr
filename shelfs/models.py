from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from os.path import join
from taggit.managers import TaggableManager

def item_image_upload_path(instance, filename):
    """
    Generate the file path for the uploaded item image.
    Path: media/<user_id>/<shelf_id>/images/<filename>
    """
    return join(
        f"{instance.shelf.owner.id}/{instance.shelf.id}/images", filename
    )

def shelf_image_upload_path(instance, filename):
    """
    Generate the file path for the uploaded item image.
    Path: media/<user_id>/<shelf_id>/images/<filename>
    """
    return join(
        f"{instance.owner.id}/{instance.id}/images", filename
    )

def item_add_images_upload_path(instance, filename):
    """
    Generate the file path for the uploaded item image.
    Path: media/<user_id>/<shelf_id>/images/<filename>
    """
    return join(
        f"{instance.item.owner.id}/{instance.item.id}/images", filename
    )

# Create your models here.
class Shelf(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(default='../static/icons/shelf.svg', upload_to=shelf_image_upload_path)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
class Item(models.Model):
    title = models.CharField(max_length=25)
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(default='../static/icons/item.svg', upload_to=item_image_upload_path)
    quantity = models.PositiveIntegerField(default=1)
    date = models.DateTimeField(default=timezone.now)
    shelf = models.ForeignKey(Shelf, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = TaggableManager(blank=True)

    def __str__(self):
        return self.title
    
class ItemImage(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    image = models.ImageField(default='../static/icons/item.svg', upload_to=item_add_images_upload_path)
