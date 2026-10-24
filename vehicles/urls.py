
from django.urls import path
from .views import vehicle_list, vehicle_search

urlpatterns = [
    path('vehicles/search/', vehicle_search, name='vehicle-search'),
    path('vehicles/', vehicle_list, name='vehicle-list'),
]
