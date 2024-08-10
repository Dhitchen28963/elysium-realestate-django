from django.shortcuts import render
from real_estate.models import Property
from real_estate.forms import PropertySearchForm

"""
Handles the display of the home page, including a property search form.
Filters properties based on search criteria entered by the user.
"""


def home(request):
    form = PropertySearchForm(request.GET)
    properties = Property.objects.all()

    if form.is_valid():
        if form.cleaned_data.get('search'):
            properties = properties.filter(
                location__icontains=form.cleaned_data['search']
            )
        if form.cleaned_data.get('location'):
            properties = properties.filter(
                location__icontains=form.cleaned_data['location']
            )
        if form.cleaned_data.get('property_type') and \
                form.cleaned_data['property_type'] != 'any':
            properties = properties.filter(
                property_type=form.cleaned_data['property_type']
            )
        if form.cleaned_data.get('bedrooms_min'):
            properties = properties.filter(
                bedrooms__gte=form.cleaned_data['bedrooms_min']
            )
        if form.cleaned_data.get('bedrooms_max'):
            properties = properties.filter(
                bedrooms__lte=form.cleaned_data['bedrooms_max']
            )
        if form.cleaned_data.get('price_min'):
            properties = properties.filter(
                price__gte=form.cleaned_data['price_min']
            )
        if form.cleaned_data.get('price_max'):
            properties = properties.filter(
                price__lte=form.cleaned_data['price_max']
            )
        if form.cleaned_data.get('garden'):
            properties = properties.filter(
                garden=form.cleaned_data['garden']
            )
        if form.cleaned_data.get('parking'):
            properties = properties.filter(
                parking=form.cleaned_data['parking']
            )
        if form.cleaned_data.get('pets_allowed'):
            properties = properties.filter(
                pets_allowed=form.cleaned_data['pets_allowed']
            )

    context = {
        'form': form,
        'properties': properties
    }
    return render(request, 'home/index.html', context)


"""
Renders the property sale page, displaying properties available for sale.
"""


def property_sale(request):
    return render(request, 'real_estate/property_sale.html')


"""
Renders the property rent page, displaying properties available for rent.
"""


def property_rent(request):
    return render(request, 'real_estate/property_rent.html')
