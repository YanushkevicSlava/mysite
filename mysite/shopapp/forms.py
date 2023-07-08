from django import forms
from .models import Product, Order
from django.forms import ModelForm
from django.contrib.auth.models import Group


# class ProductForm(forms.Form):
#     name = forms.CharField(max_length=100)
#     price = forms.DecimalField(min_value=1, max_value=100000, decimal_places=2)
#     description = forms.CharField(label="Product Description",
#                                   widget=forms.Textarea(attrs={"rows": 5}))

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "name", "price", "description", "discount", "preview"

    images = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={"allow_multiple_selected": True}), required=False
    )


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = "user", "products", "promocode"


class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ['name']


