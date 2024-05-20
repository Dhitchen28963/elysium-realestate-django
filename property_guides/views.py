from django.views.generic import ListView, DetailView
from .models import PropertyGuide

class PropertyGuidesListView(ListView):
    model = PropertyGuide
    template_name = 'property_guides/property_guides_list.html'

class PropertyGuidesDetailView(DetailView):
    model = PropertyGuide
    template_name = 'property_guides/property_guides_detail.html'
