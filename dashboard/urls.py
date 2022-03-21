from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # home
    path('order_details/', views.view_order_details, name='order_details'),
    path('order_details_ind/<str:orderid>', views.view_order_details_ind, name='order_details_ind'),
    path('send_item/<str:orderid>', views.send_item, name='send_item'),
    path('delivered/<str:orderid>', views.item_delivered, name='item_delivered'),
]
