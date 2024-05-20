from django.urls import path
from .views import TestimonialsListView, TestimonialsDetailView

urlpatterns = [
    path('', TestimonialsListView.as_view(), name='testimonials_list'),
    path('<slug:slug>/', TestimonialsDetailView.as_view(), name='testimonials_detail'),
]
