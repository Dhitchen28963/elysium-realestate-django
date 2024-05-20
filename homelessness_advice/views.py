from django.views.generic import ListView, DetailView
from .models import HomelessnessAdvice

class HomelessnessAdviceListView(ListView):
    model = HomelessnessAdvice
    template_name = 'homelessness_advice/homelessness_advice_list.html'

class HomelessnessAdviceDetailView(DetailView):
    model = HomelessnessAdvice
    template_name = 'homelessness_advice/homelessness_advice_detail.html'
