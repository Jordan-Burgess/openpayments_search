from django.urls import path
from .views import search_page, api_search

urlpatterns = [
    path('search/', search_page, name='search_page'),
    path('api/search/', api_search, name='api_search'),
]