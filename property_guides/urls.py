from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.property_guides_list, name='property_guides_list'),
    path(
        'post/<slug:slug>/',
        views.property_guides_detail,
        name='property_guides_detail'
    ),
    path(
        'category/<str:category_name>/',
        views.property_guides_category,
        name='property_guides_category'
    ),
    path(
        'repairs/',
        views.property_guides_category,
        {'category_name': 'Repairs'},
        name='repairs'
    ),
    path(
        'fire-safety/',
        views.property_guides_category,
        {'category_name': 'Fire Safety'},
        name='fire_safety'
    ),
    path(
        'complaints/',
        views.property_guides_category,
        {'category_name': 'Complaints'},
        name='complaints'
    ),
    path(
        'eviction/',
        views.property_guides_category,
        {'category_name': 'Eviction'},
        name='eviction'
    ),
    path(
        'mortgage/',
        views.property_guides_category,
        {'category_name': 'Mortgage'},
        name='mortgage'
    ),
    path(
        'buying-selling/',
        views.property_guides_category,
        {'category_name': 'Buyers/Selling'},
        name='buying_selling'
    ),
    path('summernote/', include('django_summernote.urls')),
]
