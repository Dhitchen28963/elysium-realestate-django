from django.shortcuts import render
from django.views import generic
from .models import Property

# Create your views here.
class PropertyList(generic.ListView):
    queryset = Property.objects.all()
    template_name = "property_list.html"