from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.http import JsonResponse
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from .forms import PropertySearchForm, ViewingAppointmentForm, SavedSearchForm
from .models import Property, FavoriteProperty, PropertyMessage, ViewingSlot, ViewingAppointment, SavedSearch, PropertyAlert

@login_required
def request_custom_viewing(request, property_id):
    property = get_object_or_404(Property, id=property_id)

    if request.method == 'POST':
        form = ViewingAppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.property = property
            appointment.user = request.user
            appointment.save()
            return JsonResponse({'status': 'ok'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

@login_required
def accept_appointment(request, appointment_id):
    appointment = get_object_or_404(ViewingAppointment, id=appointment_id)
    if request.method == 'POST':
        appointment.viewing_decision = 'accepted'
        appointment.save()

        # Send notification email to the user
        send_mail(
            'Your Viewing Appointment is Accepted',
            f'Dear {appointment.user.username}, your viewing appointment for {appointment.property.title} has been accepted.',
            'from@example.com',
            [appointment.user.email],
            fail_silently=False,
        )

        messages.success(request, 'The appointment has been accepted and the user has been notified.')
        return redirect('view_pending_viewings')

    context = {
        'appointment': appointment,
    }
    return render(request, 'real_estate/accept_appointment.html', context)

def property_sale(request):
    form = PropertySearchForm(request.GET)
    properties = Property.objects.filter(transaction_type='sale', publication_status='published')

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
    properties = Property.objects.filter(transaction_type='rent', publication_status='published')

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
    context = {
        'favorites': favorites
    }
    return render(request, 'real_estate/favorites.html', context)

@login_required
def remove_from_favorites(request, property_id):
    if request.method == 'POST':
        property = get_object_or_404(Property, id=property_id)
        favorite = FavoriteProperty.objects.filter(user=request.user, property=property).first()
        if favorite:
            favorite.delete()
            return JsonResponse({'status': 'ok'})
        else:
            return JsonResponse({'status': 'not_found'}, status=404)
    return JsonResponse({'status': 'error'}, status=400)

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

@login_required
def view_pending_viewings(request):
    pending_viewings = ViewingAppointment.objects.filter(user=request.user, is_scheduled=False)
    return render(request, 'real_estate/pending_viewings.html', {'pending_viewings': pending_viewings})

@login_required
def view_scheduled_viewings(request):
    scheduled_viewings = ViewingAppointment.objects.filter(user=request.user, viewing_decision='accepted')
    context = {
        'scheduled_viewings': scheduled_viewings
    }
    return render(request, 'real_estate/scheduled_viewings.html', context)

@login_required
def save_search(request):
    if request.method == 'POST':
        form = SavedSearchForm(request.POST)
        if form.is_valid():
            saved_search = form.save(commit=False)
            saved_search.user = request.user
            saved_search.save()
            return redirect('view_saved_searches')
    else:
        form = SavedSearchForm()
    return render(request, 'real_estate/save_search.html', {'form': form})

@login_required
def delete_saved_search(request, search_id):
    search = get_object_or_404(SavedSearch, id=search_id, user=request.user)
    if request.method == 'POST':
        search.delete()
        return redirect('view_saved_searches')
    return render(request, 'real_estate/delete_saved_search.html', {'search': search})

@login_required
def view_saved_searches(request):
    saved_searches = SavedSearch.objects.filter(user=request.user)
    return render(request, 'real_estate/saved_searches.html', {'saved_searches': saved_searches})

@login_required
def view_property_alerts(request):
    alerts = PropertyAlert.objects.filter(user=request.user, seen=False)
    return render(request, 'real_estate/property_alerts.html', {'alerts': alerts})

def create_property_alert(property):
    saved_searches = SavedSearch.objects.filter(
        location__icontains=property.location,
        property_type=property.property_type,
        bedrooms_min__lte=property.bedrooms,
        bedrooms_max__gte=property.bedrooms,
        price_min__lte=property.price,
        price_max__gte=property.price,
        garden=property.garden,
        parking=property.parking,
        pets_allowed=property.pets_allowed,
        furnished_type=property.furnished_type
    )
    for search in saved_searches:
        PropertyAlert.objects.create(user=search.user, property=property)

class ProfileView(TemplateView):
    template_name = 'real_estate/profile.html'

class MessagesView(TemplateView):
    template_name = 'real_estate/messages.html'

class AccountSettingsView(TemplateView):
    template_name = 'real_estate/account_settings.html'
