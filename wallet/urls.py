from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page_view, name='home'),
    path('transactions/', views.transactions_page_view, name="transactions"),
]