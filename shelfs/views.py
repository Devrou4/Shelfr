from django.shortcuts import render
from .models import Shelf

# Create your views here.

def index(request):
    context = { 'shelfs': Shelf.objects.all() }

    return render(request, 'shelfs/index.html', context)