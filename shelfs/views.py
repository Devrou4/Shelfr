from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, DetailView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Shelf, Item

# Create your views here.
@login_required
def index(request):
    context = { 'shelfs': Shelf.objects.filter(owner_id=request.user.id) }
    return render(request, 'shelfs/index.html', context)

@login_required
def shelf(request, pk):
    context = { 'items': Item.objects.filter(shelf_id=pk), 'shelf_id':pk  }
    return render(request, 'shelfs/shelf.html', context)


class ShelfCreateView(LoginRequiredMixin, CreateView):
    model = Shelf
    fields = ['title', 'content', 'image']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('shelfr-home')
    
class ShelfUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Shelf
    fields = ['title', 'content', 'image']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('shelfr-home')
    
    def test_func(self):
        shelf = self.get_object()
        if self.request.user == shelf.owner:
            return True
        return False

class ItemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    fields = ['title', 'content', 'image', 'quantity']

    def form_valid(self, form):
        shelf = get_object_or_404(Shelf, pk=self.kwargs['pk'])
        form.instance.shelf = shelf

        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('shelfr-shelf', kwargs={'pk': self.kwargs['pk']})
    
class ItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Item
    fields = ['title', 'content', 'image', 'quantity']

    def form_valid(self, form):
        shelf = get_object_or_404(Shelf, pk=self.kwargs['shelf_pk'])
        form.instance.shelf = shelf

        return super().form_valid(form)
    
    def get_success_url(self):
        item = self.get_object()
        return reverse('shelfr-item-detail', kwargs={'shelf_pk': item.shelf.id, 'pk': item.id})
    
    def test_func(self):
        item = self.get_object()
        if self.request.user == item.shelf.owner:
            return True
        return False

class ItemDetailView(LoginRequiredMixin, DetailView):
    model = Item