from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.StudentPropertyList.as_view(), name='student_accommodation'),
    path('<slug:slug>/', views.StudentPropertyDetail.as_view(), name='student_accommodation_detail'),
    path('summernote/', include('django_summernote.urls')),
]
