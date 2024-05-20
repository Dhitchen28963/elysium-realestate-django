from django.views.generic import ListView
from .models import HomelessnessAdvice

class HomelessnessAdviceListView(ListView):
    model = HomelessnessAdvice
    template_name = 'homelessness_advice/homelessness_advice_list.html'
    context_object_name = 'advices'
