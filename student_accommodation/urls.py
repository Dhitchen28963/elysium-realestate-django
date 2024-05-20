from django.urls import path
from .views import StudentAccommodationListView, StudentAccommodationDetailView

urlpatterns = [
    path('', StudentAccommodationListView.as_view(), name='student_accommodation_list'),
    path('<slug:slug>/', StudentAccommodationDetailView.as_view(), name='student_accommodation_detail'),
]
