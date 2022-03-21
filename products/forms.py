from django import forms
from .models import ProductCategories, Product, ProductComment


class ProductCategoriesForm(forms.ModelForm):
    class Meta:
        model = ProductCategories
        fields = ['name']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'photo', 'categories', 'price', 'desc', 'stock', 'discount_amt', 'is_available']
