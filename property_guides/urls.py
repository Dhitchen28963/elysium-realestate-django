from django.urls import path
from . import views

urlpatterns = [
    path('', views.property_guides_list, name='property_guides_list'),
    path('repairs/', views.repairs, name='repairs'),
    path('fire-safety/', views.fire_safety, name='fire_safety'),
    path('complaints/', views.complaints, name='complaints'),
    path('eviction/', views.eviction, name='eviction'),
    path('<slug:slug>/', views.property_guides_detail, name='property_guides_detail'),
]
