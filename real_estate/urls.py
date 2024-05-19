from django.urls import path
from . import views

urlpatterns = [
    path('property/<slug:slug>/', views.property_detail, name='property_detail'),
    path('property-sale/', views.property_sale, name='property_sale'),
    path('property-rent/', views.property_rent, name='property_rent'),
    path('add-to-favorites/<int:property_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('schedule-viewing/<int:property_id>/', views.schedule_viewing, name='schedule_viewing'),
    path('contact-agent/<int:property_id>/', views.contact_agent, name='contact_agent'),
]