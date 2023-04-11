from django import forms
from .models import ProductCategories, Product, ProductComment


class ProductCategoriesForm(forms.ModelForm):
    class Meta:
        model = ProductCategories
        fields = ['name']


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['user','name', 'photo','categories', 'price', 'desc', 'stock', 'discount_amt', 'is_available']
    
    def __init__(self, user=None, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['user'].initial = user
        self.fields['user'].widget = forms.HiddenInput()
