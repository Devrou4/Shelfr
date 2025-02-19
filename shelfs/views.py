from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from .models import Shelf, Item
from django.db.models import Q
from taggit.models import Tag
from django.http import JsonResponse
import json
from .forms import ItemForm

# Create your views here.
@login_required
def index(request):
    context = { 'shelfs': Shelf.objects.filter(owner_id=request.user.id) }
    return render(request, 'shelfs/index.html', context)

@login_required
def shelf(request, pk):
    shelf = get_object_or_404(Shelf, pk=pk)
    context = { 'items': Item.objects.filter(shelf_id=pk), 'shelf_id':pk, 'shelf':shelf  }
    return render(request, 'shelfs/shelf.html', context)

@login_required
def search(request):

    query = request.GET.get('q')
    
    shelfs = Shelf.objects.filter(owner_id=request.user.id, title__icontains=query)
    items = Item.objects.filter(Q(title__icontains=query) | Q(tags__name__icontains=query), owner_id=request.user.id).distinct()

    return render(request, 'shelfs/search.html', {'shelfs':shelfs, 'items':items})

@login_required
def tags(request):

    tags = Tag.objects.filter(item__owner=request.user).distinct()

    tags_with_items = {tag: Item.objects.filter(tags=tag, owner=request.user) for tag in tags}

    return render(request, 'shelfs/tags.html', {'tags_with_items':tags_with_items})

def reorder_shelves(request):
    if request.method == "POST":
        data = json.loads(request.body)
        for shelf in data["order"]:
            Shelf.objects.filter(id=shelf["id"]).update(order=shelf["position"])
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error"}, status=400)

def reorder_items(request):
    if request.method == "POST":
        data = json.loads(request.body)
        for item in data["order"]:
            Item.objects.filter(id=item["id"]).update(order=item["position"])
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error"}, status=400)


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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shelf = self.get_object()
        context['cancel_url'] = reverse_lazy("shelfr-shelf", kwargs={'pk': shelf.id})
        return context
    
    def test_func(self):
        shelf = self.get_object()
        if self.request.user == shelf.owner:
            return True
        return False
    

class ShelfDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Shelf
    template_name = "shelfs/confirm_delete.html"

    def get_success_url(self):
        return reverse('shelfr-home')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shelf = self.get_object()
        context['cancel_url'] = reverse_lazy("shelfr-shelf", kwargs={'pk': shelf.id})
        return context

    def test_func(self):
        shelf = self.get_object()
        if self.request.user == shelf.owner:
            return True
        return False


class ItemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    fields = ['title', 'content', 'image', 'quantity', 'tags']

    def form_valid(self, form):
        shelf = get_object_or_404(Shelf, pk=self.kwargs['pk'])
        form.instance.shelf = shelf
        form.instance.owner = self.request.user

        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('shelfr-shelf', kwargs={'pk': self.kwargs['pk']})
    

class ItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Item
    form_class = ItemForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        item = self.get_object()
        messages.success(self.request, f"{item.title} successfuly moved to {item.shelf.title}!")
        return reverse("shelfr-item-detail", kwargs={"shelf_pk": item.shelf.id, "pk": item.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = self.get_object()
        context["cancel_url"] = reverse_lazy("shelfr-item-detail", kwargs={"shelf_pk": item.shelf.id, "pk": item.id})
        return context

    def test_func(self):
        item = self.get_object()
        return self.request.user == item.shelf.owner


class ItemDetailView(LoginRequiredMixin, DetailView):
    model = Item

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = self.get_object()
        items = list(Item.objects.filter(shelf=item.shelf).distinct())

        current_index = next((i for i, obj in enumerate(items) if obj.id == item.id), None)

        context["previous_item"] = items[current_index - 1] if current_index is not None and current_index > 0 else None
        context["next_item"] = items[current_index + 1] if current_index is not None and current_index < len(items) - 1 else None
        context["items_in_shelf"] = items
        return context


class ItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Item
    template_name = "shelfs/confirm_delete.html"

    def get_success_url(self):
        item = self.get_object()
        return reverse('shelfr-shelf', kwargs={'pk': item.shelf.id})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = self.get_object()
        context['cancel_url'] = reverse_lazy("shelfr-item-detail", kwargs={'shelf_pk': item.shelf.id, 'pk': item.id})
        return context

    def test_func(self):
        item = self.get_object()
        if self.request.user == item.shelf.owner:
            return True
        return False