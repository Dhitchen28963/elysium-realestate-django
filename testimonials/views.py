from django.views.generic import ListView, DetailView
from .models import Testimonial

class TestimonialsListView(ListView):
    model = Testimonial
    template_name = 'testimonials/testimonials_list.html'

class TestimonialsDetailView(DetailView):
    model = Testimonial
    template_name = 'testimonials/testimonials_detail.html'
