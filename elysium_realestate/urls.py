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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('real_estate/', include('real_estate.urls')),
    path('accounts/', include('allauth.urls')),
    path('summernote/', include('django_summernote.urls')),
    path('property-sale/', include('real_estate.urls'), name='property_sale'),
    path('property-rent/', include('real_estate.urls'), name='property_rent'),
    path('property_guides/', include('property_guides.urls')),
    path('homelessness_advice/', include('homelessness_advice.urls')),
    path('testimonials/', include('testimonials.urls')),
    path('faq/', include('faq.urls')),
    path('blog/', include('blog.urls')),
]