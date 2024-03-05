from django.urls import path
from .views import search_page, api_search, export_to_excel

urlpatterns = [
    path('search/', search_page, name='search_page'),
    path('api/search/', api_search, name='api_search'),
    path('export_excel/', export_to_excel, name='export_excel'),
]