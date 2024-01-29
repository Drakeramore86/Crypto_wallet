from django.urls import path
from . import views

urlpatterns = [
    path('login_user/', views.loginUser, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
]