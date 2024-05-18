from django.shortcuts import render
from .models import Property


def property_sale(request):
    properties = Property.objects.filter(transaction_type='sale')
    return render(request, 'real_estate/property_sale.html', {'properties': properties})


def property_rent(request):
    properties = Property.objects.filter(transaction_type='rent')
    return render(request, 'real_estate/property_rent.html', {'properties': properties})