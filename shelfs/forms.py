from django import forms
from .models import Item, Shelf

class ItemForm(forms.ModelForm):
    shelf = forms.ModelChoiceField(queryset=Shelf.objects.none(), label="Move to Shelf")

    class Meta:
        model = Item
        fields = ["title", "content", "image", "quantity", "tags", "shelf"]

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields["shelf"].queryset = Shelf.objects.filter(owner=user)
