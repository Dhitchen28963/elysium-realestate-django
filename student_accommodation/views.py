from django.views.generic import ListView, DetailView
from .models import StudentAccommodation

class StudentAccommodationListView(ListView):
    model = StudentAccommodation
    template_name = 'student_accommodation/student_accommodation_list.html'

class StudentAccommodationDetailView(DetailView):
    model = StudentAccommodation
    template_name = 'student_accommodation/student_accommodation_detail.html'
