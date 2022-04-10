from django.contrib import admin

# Register your models here.
from .models import ProductCategories, Product, Season

admin.site.register(ProductCategories)
admin.site.register(Product)
admin.site.register(Season)
