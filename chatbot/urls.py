from django.urls import path
from . import views
from . import chatbot

app_name = 'chatbot'

urlpatterns = [
    path('', views.home, name='home'),
    path('get/', views.get_bot_response, name='response')
]
