from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('property-rent/', views.property_rent, name='property_rent'),
    path('property-sale/', views.property_sale, name='property_sale'),
    path(
        'properties/<str:location>/',
        views.property_by_location,
        name='property_by_location'
    ),
]
