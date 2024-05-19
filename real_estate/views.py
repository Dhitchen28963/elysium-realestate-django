from django.shortcuts import render, get_object_or_404
from .models import Property
from django.db.models import Q
from django.http import JsonResponse
from django.core.mail import send_mail
from django.contrib import messages
from .forms import PropertySearchForm


def property_sale(request):
    form = PropertySearchForm(request.GET)
    properties = Property.objects.filter(transaction_type='sale', status='published')

    if form.is_valid():
        if form.cleaned_data.get('search'):
            properties = properties.filter(location__icontains=form.cleaned_data['search'])
        if form.cleaned_data.get('location'):
            properties = properties.filter(location__icontains=form.cleaned_data['location'])
        if form.cleaned_data.get('property_type') and form.cleaned_data['property_type'] != 'any':
            properties = properties.filter(property_type=form.cleaned_data['property_type'])
        if form.cleaned_data.get('bedrooms_min'):
            properties = properties.filter(bedrooms__gte=form.cleaned_data['bedrooms_min'])
        if form.cleaned_data.get('bedrooms_max'):
            properties = properties.filter(bedrooms__lte=form.cleaned_data['bedrooms_max'])
        if form.cleaned_data.get('price_min'):
            properties = properties.filter(price__gte=form.cleaned_data['price_min'])
        if form.cleaned_data.get('price_max'):
            properties = properties.filter(price__lte=form.cleaned_data['price_max'])
        if form.cleaned_data.get('garden'):
            properties = properties.filter(garden=form.cleaned_data['garden'])
        if form.cleaned_data.get('parking'):
            properties = properties.filter(parking=form.cleaned_data['parking'])
        if form.cleaned_data.get('pets_allowed'):
            properties = properties.filter(pets_allowed=form.cleaned_data['pets_allowed'])

    context = {
        'form': form,
        'properties': properties
    }
    return render(request, 'real_estate/property_sale.html', context)


def property_rent(request):
    form = PropertySearchForm(request.GET)
    properties = Property.objects.filter(transaction_type='rent', status='published')

    if form.is_valid():
        if form.cleaned_data.get('search'):
            properties = properties.filter(location__icontains=form.cleaned_data['search'])
        if form.cleaned_data.get('location'):
            properties = properties.filter(location__icontains=form.cleaned_data['location'])
        if form.cleaned_data.get('property_type') and form.cleaned_data['property_type'] != 'any':
            properties = properties.filter(property_type=form.cleaned_data['property_type'])
        if form.cleaned_data.get('bedrooms_min'):
            properties = properties.filter(bedrooms__gte=form.cleaned_data['bedrooms_min'])
        if form.cleaned_data.get('bedrooms_max'):
            properties = properties.filter(bedrooms__lte=form.cleaned_data['bedrooms_max'])
        if form.cleaned_data.get('price_min'):
            properties = properties.filter(price__gte=form.cleaned_data['price_min'])
        if form.cleaned_data.get('price_max'):
            properties = properties.filter(price__lte=form.cleaned_data['price_max'])
        if form.cleaned_data.get('garden'):
            properties = properties.filter(garden=form.cleaned_data['garden'])
        if form.cleaned_data.get('parking'):
            properties = properties.filter(parking=form.cleaned_data['parking'])
        if form.cleaned_data.get('pets_allowed'):
            properties = properties.filter(pets_allowed=form.cleaned_data['pets_allowed'])
    
    context = {
        'form': form,
        'properties': properties
    }
    return render(request, 'real_estate/property_rent.html', context)


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