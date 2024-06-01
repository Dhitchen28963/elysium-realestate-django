"""
URL configuration for elysium_realestate project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from real_estate import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path("accounts/", include("allauth.urls")),
    path('summernote/', include('django_summernote.urls')),
    path('property-sale/', include('real_estate.urls'), name='property_sale'),
    path('property-rent/', include('real_estate.urls'), name='property_rent'),
    path('real_estate/', include('real_estate.urls')),
    path('student_accommodation/', include('student_accommodation.urls')),
    path('property_guides/', include('property_guides.urls')),
    path('homelessness_advice/', include('homelessness_advice.urls')),
    path('testimonials/', include('testimonials.urls')),
    path('faq/', include('faq.urls')),
    path('blog/', include('blog.urls')),
    path('add-to-favorites/<int:property_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('schedule-viewing/<int:slot_id>/', views.schedule_viewing, name='schedule_viewing'),
    path('view-property-slots/<int:property_id>/', views.view_property_slots, name='view_property_slots'),
    path('contact-property/<int:property_id>/', views.contact_property, name='contact_property'),
    path('property-slots/<int:property_id>/', views.view_property_slots, name='view_property_slots'),
    path('favorites/', views.view_favorites, name='view_favorites'),
    path('request-custom-viewing/<int:property_id>/', views.request_custom_viewing, name='request_custom_viewing'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('view-messages/', views.MessagesView.as_view(), name='view_messages'),
    path('view-search-alerts/', views.SearchAlertsView.as_view(), name='view_search_alerts'),
    path('account-settings/', views.AccountSettingsView.as_view(), name='account_settings'),
]
