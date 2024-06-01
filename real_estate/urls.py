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
    path('remove-from-favorites/<int:property_id>/', views.remove_from_favorites, name='remove_from_favorites'),
    path('favorites/', views.view_favorites, name='view_favorites'),
    path('contact-property/<int:property_id>/', views.contact_property, name='contact_property'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('messages/', views.MessagesView.as_view(), name='view_messages'),
    path('search-alerts/', views.SearchAlertsView.as_view(), name='view_search_alerts'),
    path('pending-viewings/', views.view_pending_viewings, name='pending_viewings'),
    path('accept-appointment/<int:appointment_id>/', views.accept_appointment, name='accept_appointment'),
    path('scheduled-viewings/', views.view_scheduled_viewings, name='scheduled_viewings'),
    path('account-settings/', views.AccountSettingsView.as_view(), name='account_settings'),
    
]
