from django.urls import path
from . import views

urlpatterns = [
    path('property-sale/', views.property_sale, name='property_sale'),
    path('property-rent/', views.property_rent, name='property_rent'),
]