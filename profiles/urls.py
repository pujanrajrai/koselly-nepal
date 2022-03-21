from django.urls import path
from . import views

app_name = 'my_profile'

urlpatterns = [

    path('create/', views.CreateProfile.as_view(), name='profile_create'),
    path('view/', views.ProfileListView.as_view(), name='profile_list_view'),
    path('update/', views.ProfileUpdateView.as_view(), name='profile_update'),

]
