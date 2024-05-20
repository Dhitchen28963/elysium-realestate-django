from django.views.generic import ListView
from .models import StudentAccommodation

class StudentAccommodationListView(ListView):
    model = StudentAccommodation
    template_name = 'student_accommodation/student_accommodation_list.html'
    context_object_name = 'accommodations'
