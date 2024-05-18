from django.shortcuts import render
from .models import Property
from django.db.models import Q

def property_sale(request):
    properties = Property.objects.filter(transaction_type='buy', status='published')

    # Filtering
    query = request.GET.get('q')
    property_type = request.GET.get('property_type')
    bedrooms_min = request.GET.get('bedrooms_min')
    bedrooms_max = request.GET.get('bedrooms_max')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    garden = request.GET.get('garden')
    parking = request.GET.get('parking')
    pets_allowed = request.GET.get('pets_allowed')
    furnished_type = request.GET.get('furnished_type')

    if query:
        properties = properties.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(location__icontains=query)
        )
    if property_type and property_type != 'any':
        properties = properties.filter(property_type=property_type)
    if bedrooms_min:
        properties = properties.filter(bedrooms__gte=bedrooms_min)
    if bedrooms_max:
        properties = properties.filter(bedrooms__lte=bedrooms_max)
    if price_min:
        properties = properties.filter(price__gte=price_min)
    if price_max:
        properties = properties.filter(price__lte=price_max)
    if garden:
        properties = properties.filter(garden=True)
    if parking:
        properties = properties.filter(parking=True)
    if pets_allowed:
        properties = properties.filter(pets_allowed=True)
    if furnished_type and furnished_type != 'any':
        properties = properties.filter(furnished_type=furnished_type)

    return render(request, 'real_estate/property_sale.html', {'properties': properties})

def property_rent(request):
    properties = Property.objects.filter(transaction_type='rent', status='published')

    # Filtering
    query = request.GET.get('q')
    property_type = request.GET.get('property_type')
    bedrooms_min = request.GET.get('bedrooms_min')
    bedrooms_max = request.GET.get('bedrooms_max')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    garden = request.GET.get('garden')
    parking = request.GET.get('parking')
    pets_allowed = request.GET.get('pets_allowed')
    furnished_type = request.GET.get('furnished_type')

    if query:
        properties = properties.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(location__icontains=query)
        )
    if property_type and property_type != 'any':
        properties = properties.filter(property_type=property_type)
    if bedrooms_min:
        properties = properties.filter(bedrooms__gte=bedrooms_min)
    if bedrooms_max:
        properties = properties.filter(bedrooms__lte=bedrooms_max)
    if price_min:
        properties = properties.filter(price__gte=price_min)
    if price_max:
        properties = properties.filter(price__lte=price_max)
    if garden:
        properties = properties.filter(garden=True)
    if parking:
        properties = properties.filter(parking=True)
    if pets_allowed:
        properties = properties.filter(pets_allowed=True)
    if furnished_type and furnished_type != 'any':
        properties = properties.filter(furnished_type=furnished_type)

    return render(request, 'real_estate/property_rent.html', {'properties': properties})
