from django.urls import path
from . import views

app_name = 'chats'

urlpatterns = [
    # property category
    # path('category/create/', views.PropertyCategoryCreateView.as_view(), name='property_category_create'),
    path('all/chat', views.all_chat, name='chat'),
    path('view/<str:username>', views.view_chat, name='view_chat'),
    path('new/message/<str:username>', views.new_chat, name='new_message')
]
