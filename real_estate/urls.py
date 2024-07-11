from django.urls import path, include
from . import views

urlpatterns = [
    path('property/<slug:slug>/', views.property_detail, name='property_detail'),
    path('property-sale/', views.property_sale, name='property_sale'),
    path('property-rent/', views.property_rent, name='property_rent'),
    path('student-accommodation/', views.property_student, name='student_property'),
    path('request_custom_viewing/<int:property_id>/', views.request_custom_viewing, name='request_custom_viewing'),
    path('view-property-slots/<int:property_id>/', views.view_property_slots, name='view_property_slots'),
    path('add-to-favorites/<int:property_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('remove-from-favorites/<int:property_id>/', views.remove_from_favorites, name='remove_from_favorites'),
    path('favorites/', views.view_favorites, name='view_favorites'),
    path('summernote/', include('django_summernote.urls')),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('pending-viewings/', views.view_pending_viewings, name='view_pending_viewings'),
    path('update-viewing/<int:viewing_id>/', views.update_viewing, name='update_viewing'),
    path('delete_viewing/<int:viewing_id>/', views.delete_viewing, name='delete_viewing'),
    path('accept-appointment/<int:appointment_id>/', views.accept_appointment, name='accept_appointment'),
    path('account-settings/', views.account_settings, name='account_settings'),
    path('mortgage_calculator/', views.mortgage_calculator, name='mortgage_calculator'),
    path('view-land/', views.view_land, name='view_land'),
    path('repairs/', views.repairs, name='repairs'),
    path('fire-safety/', views.fire_safety, name='fire_safety'),
    path('complaints/', views.complaints, name='complaints'),
    path('eviction/', views.eviction, name='eviction'),
]