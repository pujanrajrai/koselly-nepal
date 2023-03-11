from django.urls import path, include
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('change/password', views.password_change, name='password_change'),
    # path('login/', views.login, name='login'),
    path('', views.login, name='login'),

    path('send/email/verification', views.send_email_verification_code, name='send_email_verification_code'),
    path('email/verify', views.verify_email, name='verify_email'),
    path('logout', views.logout, name='logout'),
    path('forget/password', views.forger_password, name='forger_password')
]
