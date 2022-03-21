from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    # home
    path('', views.home, name='home'),
    path('product/<str:pk>', views.product_desc, name='product_desc'),
    path('search/', views.search, name='search'),
    path('all_product/', views.view_all_product, name='view_all_product'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/', views.remove_cart, name='remove_cart'),
    path('add_subtract_cart_item/', views.add_subtract_cart_item, name='add_subtract_cart_item'),
    path('view_cart/', views.show_cart, name='show_cart'),
    path('my_order/', views.my_order, name='my_order'),
    path('order_details/<str:orderid>', views.view_order_details, name='view_order_details'),
    path('check_out/', views.checkout, name='checkout'),
    path('esewa/pay/<str:orderid>/<str:price>/', views.esewa_pay, name='esewa_pay'),
    path('esewa/success/', views.esewa_success, name='esewa_success'),
    path('esewa/faliure/', views.esewa_failure, name='esewa_failure'),
]

