from django.urls import path
from .views import main_page_view, search_address

urlpatterns = [
    path('', main_page_view, name='home'),
    path('search/', search_address, name='search_address'),
]