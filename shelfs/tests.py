from django.test import TestCase
from .models import Shelf, Item
from django.contrib.auth.models import User


class ShelfTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user("Test User", password="password")
        self.shelf = Shelf.objects.create(title="Test Shelf", owner=self.user)


    def test_create_shelf(self):
        shelf = Shelf.objects.create(title="Shelf 1", owner=self.user)
        self.assertEqual(shelf.title, "Shelf 1")
        self.assertEqual(shelf.owner.username, "Test User")


class ItemTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user("Test User", password="password")
        self.shelf = Shelf.objects.create(title="Test Shelf", owner=self.user)

    def test_create_item(self):
        item = Item.objects.create(title="Item 1", shelf=self.shelf, owner=self.user)
        self.assertEqual(item.title, "Item 1")
        self.assertEqual(item.shelf.title, "Test Shelf")

    def test_shelf_deletion_cascades_items(self):
        Item.objects.create(title="Item 1", shelf=self.shelf, owner=self.user)
        self.shelf.delete()
        
        self.assertEqual(Item.objects.count(), 0)

    def test_item_default_quantity(self):
        item = Item.objects.create(title="Item 1", shelf=self.shelf, owner=self.user)
        self.assertEqual(item.quantity, 1)
