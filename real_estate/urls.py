from django.urls import path
from . import views

urlpatterns = [
    path('property/<slug:slug>/', views.property_detail, name='property_detail'),
    path('property-sale/', views.property_sale, name='property_sale'),
    path('property-rent/', views.property_rent, name='property_rent'),
    path('schedule-viewing/<int:property_id>/', views.schedule_viewing, name='schedule_viewing'),
    path('request-viewing/<int:property_id>/', views.request_custom_viewing, name='request_custom_viewing'),
    path('view-property-slots/<int:property_id>/', views.view_property_slots, name='view_property_slots'),
    path('request-custom-viewing/<int:property_id>/', views.request_custom_viewing, name='request_custom_viewing'),
    path('add-to-favorites/<int:property_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('favorites/', views.view_favorites, name='view_favorites'),
    path('contact-property/<int:property_id>/', views.contact_property, name='contact_property'),
]