from django.contrib import admin

# Register your models here.
from .models import ProductCategories, Product
admin.site.register(ProductCategories)
admin.site.register(Product)

