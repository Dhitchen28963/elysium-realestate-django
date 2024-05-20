from django.urls import path
from .views import StudentAccommodationListView

urlpatterns = [
    path('', StudentAccommodationListView.as_view(), name='student_accommodation_list'),
]
