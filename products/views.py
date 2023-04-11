from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView
from .models import ProductCategories, Product

from .forms import ProductCategoriesForm, ProductForm
from django.db.models import Q

# Create your views here.


class ProductCategoriesListView(ListView):
    model = ProductCategories
    context_object_name = 'categories'
    template_name = 'products/category_list_view.html'


class ProductCategoriesCreatView(CreateView):
    form_class = ProductCategoriesForm
    success_url = '/product/category/list/'
    template_name = 'products/categories_create_view.html'


class ProductCategoryUpdateView(UpdateView):
    form_class = ProductCategoriesForm
    model = ProductCategories
    template_name = 'products/categories_create_view.html'
    success_url = '/product/category/list/'
    success_message = 'Product Category Updated Successfully'


class ProductCreateView(CreateView):
    form_class = ProductForm
    success_url = '/product/list/'
    template_name = 'products/product_create_update.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class ProductListView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'products/product_list_view.html'

    def get_queryset(self):

        queryset = Product.objects.all()

        return queryset


class ProductUpdateView(UpdateView):
    form_class = ProductForm
    model = Product
    template_name = 'products/product_create_update.html'
    success_url = '/product/list/'
    success_message = 'Product Updated Successfully'
