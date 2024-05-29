from django.urls import path
from . import views

urlpatterns = [
    path('login_user/', views.loginUser, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('profile/delete_favorite_address/<int:address_id>/', views.delete_favorite_address, name='delete_favorite_address'),
]