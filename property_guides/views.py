from django.views.generic import ListView
from .models import PropertyGuide

class PropertyGuideListView(ListView):
    model = PropertyGuide
    template_name = 'property_guides/property_guide_list.html'
    context_object_name = 'guides'
