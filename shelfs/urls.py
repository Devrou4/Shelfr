from django.urls import path
from .views import ShelfCreateView, ItemCreateView, ItemDetailView
from . import views

urlpatterns = [
    path('', views.index, name='shelfr-home'),
    path('shelf/<int:pk>/', views.shelf, name='shelfr-shelf'),
    path('shelf/new/', ShelfCreateView.as_view(), name='shelfr-shelf-new'),
    path('shelf/<int:pk>/new/', ItemCreateView.as_view(), name='shelfr-item-new'),
    path('shelf/<int:shelf_pk>/<int:pk>/', ItemDetailView.as_view(), name='shelfr-item-detail'),
]