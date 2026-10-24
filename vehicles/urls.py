
from django.urls import path
from .views import vehicle_list, vehicle_search, vehicle_detail

urlpatterns = [
    path('vehicles/search/', vehicle_search, name='vehicle-search'),
    path('vehicles/<int:pk>/', vehicle_detail, name='vehicle-detail'),
    path('vehicles/', vehicle_list, name='vehicle-list'),
]
