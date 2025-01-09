from django.shortcuts import render, redirect
from real_estate.models import Property
from real_estate.forms import PropertySearchForm
from django.db.models import Count, Q
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse

"""
Handles the display of the home page, including a property search form.
Filters properties based on search criteria entered by the user.
"""


def home(request):
    form = PropertySearchForm(request.GET)
    properties = Property.objects.all()

    if form.is_valid():
        search_query = form.cleaned_data.get('search')
        if search_query:
            properties = properties.filter(location__icontains=search_query)

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

    # Get popular and all locations for rent and sale separately
    popular_locations_rent = get_popular_locations('rent')
    popular_locations_sale = get_popular_locations('sale')
    all_locations_rent = get_all_locations('rent')
    all_locations_sale = get_all_locations('sale')

    # Debugging Outputs
    print("Search Query:", search_query)
    print("Popular Rent Locations:", popular_locations_rent)
    print("Popular Sale Locations:", popular_locations_sale)
    print("All Rent Locations:", all_locations_rent)
    print("All Sale Locations:", all_locations_sale)

    context = {
        'form': form,
        'properties': properties,
        'search_query': search_query,
        'popular_locations_rent': list(popular_locations_rent.items()),
        'popular_locations_sale': list(popular_locations_sale.items()),
        'all_locations_rent': all_locations_rent,
        'all_locations_sale': all_locations_sale,
    }
    return render(request, 'home/index.html', context)


"""
Helper function to get popular locations for a specific transaction type.
"""


def get_popular_locations(transaction_type):
    """
    Finds the top 5 most popular locations for the specified transaction type.
    """
    locations = (
        Property.objects.filter(transaction_type=transaction_type)
        .values('location')
        .annotate(property_count=Count('id'))
        .order_by('-property_count')[:5]
    )

    # Debugging: Split long line
    print("Transaction Type:", transaction_type)
    print("Popular Locations:", list(locations))

    return {
        loc['location']: {'count': loc['property_count']}
        for loc in locations
    }


"""
Helper function to get all unique locations for a specific transaction type.
"""


def get_all_locations(transaction_type):
    """
    Retrieves all unique locations for the specified transaction type.
    """
    locations = list(
        Property.objects.filter(transaction_type=transaction_type)
        .values_list('location', flat=True)
        .distinct()
    )

    print(f"Transaction Type: {transaction_type}, All Locations: {locations}")

    return locations


"""
Handles redirection based on location and transaction type.
"""


def property_by_location(request, location):
    """
    Redirects to the appropriate page (rent or sale) based on the location
    and displays all properties for that location.
    """
    location_properties = Property.objects.filter(location__iexact=location)
    rent_count = location_properties.filter(transaction_type='rent').count()
    sale_count = location_properties.filter(transaction_type='sale').count()

    target_page = (
        'property_rent' if rent_count > sale_count else 'property_sale'
    )
    url = f"{reverse(target_page)}?search={location}"
    return HttpResponseRedirect(url)


"""
Renders the property sale page, displaying properties available for sale.
"""


def property_sale(request):
    search = request.GET.get('search', '')
    properties = Property.objects.filter(
        Q(location__icontains=search) & Q(transaction_type='sale')
    )
    context = {'properties': properties, 'search': search}
    return render(request, 'real_estate/property_sale.html', context)


"""
Renders the property rent page, displaying properties available for rent.
"""


def property_rent(request):
    search = request.GET.get('search', '')
    properties = Property.objects.filter(
        Q(location__icontains=search) & Q(transaction_type='rent')
    )
    context = {'properties': properties, 'search': search}
    return render(request, 'real_estate/property_rent.html', context)
