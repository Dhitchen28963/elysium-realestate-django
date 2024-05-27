from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.http import JsonResponse
from django.core.mail import send_mail
from django.contrib import messages
from .forms import PropertySearchForm, ViewingAppointmentForm
from django.contrib.auth.decorators import login_required
from .models import Property, FavoriteProperty, PropertyMessage, ViewingSlot, ViewingAppointment
import logging

logger = logging.getLogger(__name__)

@login_required
def request_custom_viewing(request, property_id):
    property = get_object_or_404(Property, id=property_id)

    if request.method == 'POST':
        logger.info("Received POST data: %s", request.POST)
        form = ViewingAppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.property = property
            appointment.user = request.user
            appointment.save()

            # send_mail logic here if needed

            return JsonResponse({'status': 'ok'})
        else:
            logger.error("Form errors: %s", form.errors)
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

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


def contact_agent(request, property_id):
    if request.method == 'POST':
        property = get_object_or_404(Property, id=property_id)
        message = request.POST.get('message')
        return JsonResponse({'status': 'message sent'})
    return JsonResponse({'status': 'error'}, status=400)


@login_required
def add_to_favorites(request, property_id):
    if request.method == 'POST':
        property = get_object_or_404(Property, id=property_id)
        favorite, created = FavoriteProperty.objects.get_or_create(user=request.user, property=property)
        if created:
            return JsonResponse({'status': 'ok'})
        else:
            return JsonResponse({'status': 'exists'})
    return JsonResponse({'status': 'error'}, status=400)


@login_required
def view_favorites(request):
    favorites = FavoriteProperty.objects.filter(user=request.user)
    context = {'favorites': favorites}
    return render(request, 'real_estate/favorites.html', context)


@login_required
def contact_property(request, property_id):
    if request.method == 'POST':
        property = get_object_or_404(Property, id=property_id)
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        PropertyMessage.objects.create(
            property=property,
            user=request.user,
            name=name,
            email=email,
            message=message
        )
        return JsonResponse({'status': 'message sent'})
    return JsonResponse({'status': 'error'}, status=400)


@login_required
def schedule_viewing(request, slot_id):
    if request.method == 'POST':
        slot = get_object_or_404(ViewingSlot, id=slot_id, is_booked=False)
        ViewingAppointment.objects.create(slot=slot, user=request.user, property=slot.property)
        slot.is_booked = True
        slot.save()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'}, status=400)


@login_required
def view_property_slots(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    slots = ViewingSlot.objects.filter(property=property, is_booked=False).order_by('date', 'start_time')
    context = {
        'property': property,
        'slots': slots
    }
    return render(request, 'real_estate/viewing_slots.html', context)