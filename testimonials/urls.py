from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.testimonials_list, name='testimonials_list'),
    path('<int:pk>/', views.testimonials_detail, name='testimonials_detail'),
    path('add/', views.add_testimonial, name='add_testimonial'),
    path('<int:pk>/edit/', views.edit_testimonial, name='edit_testimonial'),
    path('<int:pk>/delete/', views.delete_testimonial, name='delete_testimonial'),
    path('summernote/', include('django_summernote.urls')),
]
