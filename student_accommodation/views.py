from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import StudentProperty

class StudentPropertyList(View):
    def get(self, request, *args, **kwargs):
        properties = StudentProperty.objects.order_by('-created_on')
        return render(request, 'student_accommodation/student_accommodation.html', {'properties': properties})

class StudentPropertyDetail(View):
    def get(self, request, slug, *args, **kwargs):
        property = get_object_or_404(StudentProperty, slug=slug)
        return render(request, 'student_accommodation/student_accommodation_detail.html', {'property': property})
