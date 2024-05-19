from django.shortcuts import render, get_object_or_404
from .models import Property
from django.db.models import Q
from django.http import JsonResponse
from django.core.mail import send_mail
from django.contrib import messages

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


def property_detail(request, slug):
    property = get_object_or_404(Property, slug=slug)
    context = {
        'property': property,
        'additional_images': property.property_images.all(),
    }
    return render(request, 'real_estate/property_detail.html', context)


def add_to_favorites(request, property_id):
    if request.method == 'POST':
        property = get_object_or_404(Property, id=property_id)
        # Add logic to save the property to the user's favorites
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'}, status=400)


def schedule_viewing(request, property_id):
    if request.method == 'POST':
        property = get_object_or_404(Property, id=property_id)
        # Add logic to schedule a viewing
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'}, status=400)


def contact_agent(request, property_id):
    if request.method == 'POST':
        property = get_object_or_404(Property, id=property_id)
        message = request.POST.get('message')
        # Add logic to send a message to the agent
        return JsonResponse({'status': 'message sent'})
    return JsonResponse({'status': 'error'}, status=400)


def contact_property(request, property_id):
    property = get_object_or_404(Property, id=property_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Send an email to the agent (replace with actual email sending logic)
        send_mail(
            f'Property Inquiry: {property.title}',
            f'Name: {name}\nEmail: {email}\n\nMessage:\n{message}',
            email,
            ['agent@example.com'],  # Replace with the agent's email address
        )

        messages.success(request, 'Your message has been sent to the agent.')
        return redirect('property_detail', slug=property.slug)

    return render(request, 'real_estate/property_detail.html', {'property': property})