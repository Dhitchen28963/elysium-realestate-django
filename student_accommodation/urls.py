from django.urls import path
from . import views

urlpatterns = [
    path('', views.StudentPropertyList.as_view(), name='student_accommodation'),
    path('<slug:slug>/', views.StudentPropertyDetail.as_view(), name='student_accommodation_detail'),
]
