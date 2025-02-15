from django import forms
from .models import Item, ItemImage

class ItemForm(forms.ModelForm):
    additional_images = forms.FileField(widget = forms.TextInput(attrs={
            "name": "images",
            "type": "File",
            "class": "form-control",
            "multiple": "True",
        }), label = "Additional Images", required=False)

    class Meta:
        model = Item
        fields = ['title', 'content', 'image', 'additional_images', 'quantity', 'tags']

    def save(self, commit=True):
        instance = super().save(commit=commit)
        return instance
