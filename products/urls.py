from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    # property category
    path('category/create/', views.ProductCategoriesCreatView.as_view(), name='product_category_create'),
    path('category/list/', views.ProductCategoriesListView.as_view(), name='product_category_list'),
    path('category/update/<str:pk>', views.ProductCategoryUpdateView.as_view(), name='product_category_update'),

    # product
    path('list/', views.ProductListView.as_view(), name='product_list'),
    path('create/', views.ProductCreateView.as_view(), name='product_create'),
    path('update/<str:pk>', views.ProductUpdateView.as_view(), name='product_update'),
]
