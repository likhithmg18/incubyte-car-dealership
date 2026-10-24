
from django.urls import path

from .views import (
    vehicle_list,
    vehicle_search,
    vehicle_detail,
    purchase_vehicle,
    restock_vehicle,
)
from .auth_views import RegisterView, LoginView


urlpatterns = [
    # Authentication endpoints
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),

    # Vehicle search
    path('vehicles/search/', vehicle_search, name='vehicle-search'),

    # Purchase and restock
    path(
        'vehicles/<int:pk>/purchase/',
        purchase_vehicle,
        name='vehicle-purchase',
    ),
    path(
        'vehicles/<int:pk>/restock/',
        restock_vehicle,
        name='vehicle-restock',
    ),

    # Vehicle details, listing and creation
    path('vehicles/<int:pk>/', vehicle_detail, name='vehicle-detail'),
    path('vehicles/', vehicle_list, name='vehicle-list'),
]
