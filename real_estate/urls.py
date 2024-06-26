from django.urls import path
from . import views

urlpatterns = [
    path('property/<slug:slug>/', views.property_detail, name='property_detail'),
    path('property-sale/', views.property_sale, name='property_sale'),
    path('property-rent/', views.property_rent, name='property_rent'),
    path('schedule-viewing/<int:property_id>/', views.schedule_viewing, name='schedule_viewing'),
    path('view-property-slots/<int:property_id>/', views.view_property_slots, name='view_property_slots'),
    path('request-custom-viewing/<int:property_id>/', views.request_custom_viewing, name='request_custom_viewing'),
    path('send-message/<int:property_id>/', views.send_message, name='real_estate_send_message'),
    path('add-to-favorites/<int:property_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('remove-from-favorites/<int:property_id>/', views.remove_from_favorites, name='remove_from_favorites'),
    path('favorites/', views.view_favorites, name='view_favorites'),
    path('contact-property/<int:property_id>/', views.contact_property, name='contact_property'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('messages/', views.view_messages, name='view_messages'),
    path('messages/delete/<int:message_id>/', views.delete_message, name='delete_message'),
    path('save-search/', views.save_search, name='save_search'),
    path('delete-saved-search/<int:search_id>/', views.delete_saved_search, name='delete_saved_search'),
    path('saved-searches/', views.view_saved_searches, name='view_saved_searches'),
    path('property-alerts/', views.view_property_alerts, name='view_property_alerts'),
    path('pending-viewings/', views.view_pending_viewings, name='pending_viewings'),
    path('accept-appointment/<int:appointment_id>/', views.accept_appointment, name='accept_appointment'),
    path('scheduled-viewings/', views.view_scheduled_viewings, name='scheduled_viewings'),
    path('account-settings/', views.account_settings, name='account_settings'),
]