from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Shelf, Item

# Create your views here.
@login_required
def index(request):
    context = { 'shelfs': Shelf.objects.filter(owner_id=request.user.id) }
    return render(request, 'shelfs/index.html', context)

@login_required
def shelf(request, pk):
    context = { 'items': Item.objects.filter(shelf_id=pk) }
    return render(request, 'shelfs/shelf.html', context)


class ShelfCreateView(LoginRequiredMixin, CreateView):
    model = Shelf
    fields = ['title', 'content', 'image']