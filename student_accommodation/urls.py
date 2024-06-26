from django.urls import path
from . import views

urlpatterns = [
    path('', views.StudentPropertyList.as_view(), name='student_accommodation'),
    path('property/<slug:slug>/', views.StudentPropertyDetail.as_view(), name='student_property_detail'),
    path('rent/', views.student_property_rent, name='student_property_rent'),
    path('schedule-viewing/<int:slot_id>/', views.schedule_student_viewing, name='schedule_student_viewing'),
    path('request-viewing/<int:property_id>/', views.request_student_custom_viewing, name='request_student_custom_viewing'),
    path('view-property-slots/<int:property_id>/', views.view_student_property_slots, name='view_student_property_slots'),
    path('request-custom-viewing/<int:property_id>/', views.request_student_custom_viewing, name='request_student_custom_viewing'),
    path('send-message/<int:property_id>/', views.send_message, name='send_message'),
    path('add-to-favorites/<int:property_id>/', views.add_student_property_to_favorites, name='add_student_property_to_favorites'),
    path('remove-from-favorites/<int:property_id>/', views.remove_student_property_from_favorites, name='remove_student_property_from_favorites'),
    path('favorites/', views.view_student_favorites, name='view_student_favorites'),
    path('contact-property/<int:property_id>/', views.contact_student_property, name='contact_student_property'),
    path('profile/', views.StudentProfileView.as_view(), name='student_profile'),
    path('messages/', views.StudentMessagesView.as_view(), name='view_student_messages'),
    path('search-alerts/', views.view_student_property_alerts, name='view_student_search_alerts'),
    path('save-search/', views.save_student_search, name='save_student_search'),
    path('saved-searches/', views.view_student_saved_searches, name='view_student_saved_searches'),
    path('property-alerts/', views.view_student_property_alerts, name='view_student_property_alerts'),
    path('pending-viewings/', views.view_pending_student_viewings, name='pending_student_viewings'),
    path('accept-appointment/<int:appointment_id>/', views.accept_student_appointment, name='accept_student_appointment'),
    path('schedule-viewing/', views.schedule_student_viewing, name='schedule_student_viewing'),
    path('account-settings/', views.StudentAccountSettingsView.as_view(), name='student_account_settings'),
]
