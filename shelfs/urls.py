from django.urls import path
from .views import ShelfCreateView
from . import views

urlpatterns = [
    path('', views.index, name='shelfr-home'),
    path('shelf/<int:pk>/', views.shelf, name='shelfr-shelf'),
    path('shelf/new/', ShelfCreateView.as_view(), name='shelfr-shelf-new'),
]