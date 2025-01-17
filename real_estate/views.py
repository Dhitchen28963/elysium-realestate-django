from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView
from .forms import (
    PropertySearchForm, ViewingAppointmentForm, ProfileUpdateForm,
    ChangePasswordForm, DeleteAccountForm
)
from .models import (
    Property, FavoriteProperty, ViewingSlot, ViewingAppointment, Profile
)
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.conf import settings
import requests
import json
from datetime import date, time
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.db.models import Count, Q
from .forms import PropertySearchForm
from .models import Property

# Helper function to paginate properties


def paginate_properties(request, properties, per_page=20):
    page = request.GET.get('page', 1)
    paginator = Paginator(properties, per_page)
    try:
        properties = paginator.page(page)
    except PageNotAnInteger:
        properties = paginator.page(1)
    except EmptyPage:
        properties = paginator.page(paginator.num_pages)
    return properties, paginator

# View to request a custom viewing appointment for a property


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
            return JsonResponse(
                {'status': 'error', 'errors': form.errors}, status=400
            )
    else:
        form = ViewingAppointmentForm()
    return render(
        request, 'request_custom_viewing.html',
        {'form': form, 'property': property}
    )

# View to book a specific viewing slot


@login_required
def book_viewing_slot(request, slot_id):
    try:
        # Validate that the slot exists
        slot = ViewingSlot.objects.get(id=slot_id)
    except ViewingSlot.DoesNotExist:
        return JsonResponse(
            {'status': 'error', 'message': 'Slot not found.'},
            status=404
        )

    if request.method == 'POST':
        try:
            # Decode the JSON body
            data = json.loads(request.body)

            # Validate required fields
            name = data.get('name')
            contact = data.get('contact')
            email = data.get('email')

            if not all([name, contact, email]):
                return JsonResponse({
                    'status': 'error',
                    'message': 'Name, contact, and email are required.'
                }, status=400)

            # Create ViewingAppointment
            appointment = ViewingAppointment.objects.create(
                user=request.user,
                property=slot.property,
                slot=slot,
                name=name,
                contact=contact,
                email=email,
                preferred_date=slot.date,
                preferred_time=slot.start_time,
                viewing_decision='pending'
            )

            # Mark slot as booked
            slot.is_booked = True
            slot.save()

            return JsonResponse(
                {'status': 'ok', 'message': 'Slot successfully booked.'})
        except json.JSONDecodeError:
            return JsonResponse(
                {'status': 'error', 'message': 'Invalid JSON data.'},
                status=400
            )
        except Exception:
            return JsonResponse(
                {
                    'status': 'error',
                    'message': 'An unexpected error occurred.'
                },
                status=500
            )

    # If not a POST request, return an error
    return JsonResponse(
        {'status': 'error', 'message': 'Invalid request method.'},
        status=40
    )


# View to retrieve available viewing slots for a specific property


@login_required
def view_property_slots(request, property_id):
    try:
        # Get the property
        property = get_object_or_404(Property, id=property_id)

        # Fix invalid slots before querying
        ViewingSlot.objects.filter(
            property=property,
            is_booked=True,
            end_time__lte=time(0, 0)
        ).update(is_booked=False, end_time=time(23, 59))

        # Query for available slots
        slots = ViewingSlot.objects.filter(
            property=property,
            is_booked=False,
            date__gte=date.today()  # Filter for future dates
        ).order_by('date', 'start_time')

        # Format slots for JSON response
        slots_list = [
            {
                'id': slot.id,
                'date': slot.date.strftime('%Y-%m-%d'),
                'start_time': slot.start_time.strftime('%H:%M'),
                'end_time': slot.end_time.strftime('%H:%M'),
                'formatted_date': slot.date.strftime('%B %d, %Y'),
                'formatted_time': (
                    f"{slot.start_time.strftime('%I:%M %p')} - "
                    f"{slot.end_time.strftime('%I:%M %p')}"
                ),
            }
            for slot in slots
        ]

        return JsonResponse({'slots': slots_list})
    except Exception:
        return JsonResponse(
            {'error': 'Error fetching available slots'}, status=500
        )


# View to accept a viewing appointment


@login_required
def accept_appointment(request, appointment_id):
    appointment = get_object_or_404(ViewingAppointment, id=appointment_id)
    if request.method == 'POST':
        appointment.viewing_decision = 'accepted'
        appointment.save()

        send_mail(
            'Your Viewing Appointment is Accepted',
            f'Dear {appointment.user.username}, your viewing appointment for '
            f'{appointment.property.title} has been accepted.',
            'from@example.com',
            [appointment.user.email],
            fail_silently=False,
        )

        messages.success(
            request,
            'The appointment has been accepted and the user has been notified.'
        )
        return redirect('view_pending_viewings')

    context = {
        'appointment': appointment,
    }
    return render(request, 'real_estate/accept_appointment.html', context)

# Helper function to filter properties based on form data


def filter_properties(form, properties):
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
    return properties


# Helper function to get popular locations for a specific transaction type


def get_popular_locations(transaction_type):
    locations = (
        Property.objects.filter(transaction_type=transaction_type)
        .values('location')
        .annotate(property_count=Count('id'))
        .order_by('-property_count')[:5]
    )
    return {
        loc['location']: {'count': loc['property_count']}
        for loc in locations
    }

# Helper function to get all unique locations for a specific transaction type


def get_all_locations(transaction_type):
    locations = list(
        Property.objects.filter(transaction_type=transaction_type)
        .values_list('location', flat=True)
        .distinct()
    )
    return locations


"""
Handles redirection based on location and transaction type.
"""


def property_by_location(request, location):
    """
    Redirects to the appropriate page based on location and transaction type.
    Displays all properties for the selected location.
    """
    # Get the transaction type from the query string
    transaction_type = request.GET.get('type')

    # Map transaction types to their respective view names
    transaction_type_mapping = {
        'rent': 'property_rent',
        'sale': 'property_sale',
        'student': 'student_property',
        'land': 'view_land',
    }

    # Validate the transaction type and redirect to the correct page
    if transaction_type in transaction_type_mapping:
        return HttpResponseRedirect(
            f"{reverse(transaction_type_mapping[transaction_type])}"
            f"?search={location}"
        )

    # If transaction type is invalid, show an error and redirect to home
    messages.error(
        request,
        (
            "Invalid transaction type specified. "
            "Please select a valid property type."
        )
    )
    return redirect('home')


# View to display properties for sale


def property_sale(request):
    form = PropertySearchForm(request.GET or None)
    properties = Property.objects.filter(
        transaction_type='sale', publication_status='published'
    )

    if form.is_valid() and any(form.cleaned_data.values()):
        properties = filter_properties(form, properties)

    properties, paginator = paginate_properties(request, properties)

    context = {
        'form': form,
        'properties': properties,
        'paginator': paginator,
        'popular_locations_sale': get_popular_locations('sale'),
        'all_locations_sale': get_all_locations('sale'),
    }
    return render(request, 'real_estate/property_sale.html', context)

# View to display properties for rent


def property_rent(request):
    form = PropertySearchForm(request.GET or None)
    properties = Property.objects.filter(
        transaction_type='rent', publication_status='published'
    )

    if form.is_valid() and any(form.cleaned_data.values()):
        properties = filter_properties(form, properties)

    properties, paginator = paginate_properties(request, properties)

    context = {
        'form': form,
        'properties': properties,
        'paginator': paginator,
        'is_paginated': paginator.num_pages > 1,
        'view_title': 'rent',
        'popular_locations_rent': get_popular_locations('rent'),
        'all_locations_rent': get_all_locations('rent'),
    }
    return render(request, 'real_estate/property_rent.html', context)

# View to display student accommodation properties


def property_student(request):
    form = PropertySearchForm(request.GET)
    properties = Property.objects.filter(
        transaction_type='student', publication_status='published'
    )

    if form.is_valid() and any(form.cleaned_data.values()):
        properties = filter_properties(form, properties)

    properties, paginator = paginate_properties(request, properties)

    context = {
        'form': form,
        'properties': properties,
        'paginator': paginator,
        'is_paginated': paginator.num_pages > 1,
        'popular_locations_student': get_popular_locations('student'),
        'all_locations_student': get_all_locations('student'),
    }
    return render(request, 'real_estate/student_property.html', context)

# View to display land properties


def view_land(request):
    form = PropertySearchForm(request.GET)
    properties = Property.objects.filter(
        transaction_type='land', publication_status='published'
    )

    if form.is_valid() and any(form.cleaned_data.values()):
        properties = filter_properties(form, properties)

    properties, paginator = paginate_properties(request, properties)

    context = {
        'form': form,
        'properties': properties,
        'paginator': paginator,
        'is_paginated': paginator.num_pages > 1,
        'popular_locations_land': get_popular_locations('land'),
        'all_locations_land': get_all_locations('land'),
    }
    return render(request, 'real_estate/view_land.html', context)

# View to display the details of a specific property


def property_detail(request, slug):
    property = get_object_or_404(Property, slug=slug)
    context = {
        'property': property,
        'additional_images': property.property_images.all(),
    }
    return render(request, 'real_estate/property_detail.html', context)

# View to add a property to the user's favorites


@login_required
def add_to_favorites(request, property_id):
    if request.method == 'POST':
        property = get_object_or_404(Property, id=property_id)
        favorite, created = FavoriteProperty.objects.get_or_create(
            user=request.user, property=property
        )
        if created:
            return JsonResponse({'status': 'ok'})
        else:
            return JsonResponse({'status': 'exists'})
    return JsonResponse({'status': 'error'}, status=400)

# View to display the user's favorite properties


@login_required
def view_favorites(request):
    favorites = FavoriteProperty.objects.filter(user=request.user)
    context = {
        'favorites': favorites
    }
    return render(request, 'real_estate/favorites.html', context)

# View to remove a property from the user's favorites


@login_required
def remove_from_favorites(request, property_id):
    if request.method == 'POST':
        property = get_object_or_404(Property, id=property_id)
        favorite = FavoriteProperty.objects.filter(
            user=request.user, property=property
        ).first()
        if favorite:
            favorite.delete()
            return JsonResponse({'status': 'ok'})
        else:
            return JsonResponse({'status': 'not_found'}, status=404)
    return JsonResponse({'status': 'error'}, status=400)

# View to display the user's pending viewings


@login_required
def view_pending_viewings(request):
    """View to display the user's pending viewings."""
    try:
        # Get user's pending viewings
        viewings = ViewingAppointment.objects.filter(user=request.user)

        # Check slot availability for each viewing
        for viewing in viewings:
            viewing.slots_available = ViewingSlot.objects.filter(
                property=viewing.property,
                is_booked=False,
                date__gte=date.today()  # Filter for future slots
            ).exists()

        context = {
            'viewings': viewings,
        }
        return render(request, 'real_estate/pending_viewings.html', context)
    except Exception:
        messages.error(
            request,
            'An error occurred while fetching pending viewings.'
        )
        return redirect('home')


# View to update a specific viewing appointment


@login_required
def update_viewing(request, viewing_id):
    """Updated view for handling viewing updates with better error handling"""
    viewing = get_object_or_404(
        ViewingAppointment, id=viewing_id, user=request.user
    )

    if request.method == 'POST':
        try:
            form = ViewingAppointmentForm(request.POST, instance=viewing)
            if form.is_valid():
                # Check if preferred date/time conflicts with any booked slots
                preferred_date = form.cleaned_data['preferred_date']
                preferred_time = form.cleaned_data['preferred_time']

                # Check if there are any available slots on the preferred date
                available_slots = ViewingSlot.objects.filter(
                    property=viewing.property,
                    date=preferred_date,
                    is_booked=False
                )

                viewing = form.save(commit=False)

                # Mark as pending until approved if no available matching slots
                if not available_slots.exists():
                    viewing.viewing_decision = 'pending'
                    message = (
                        'Viewing updated successfully. '
                        'Your request will be reviewed by our team.'
                    )
                else:
                    # Check if the time matches any available slot
                    time_matches = any(
                        slot.start_time <= preferred_time <= slot.end_time
                        for slot in available_slots
                    )
                    if not time_matches:
                        viewing.viewing_decision = 'pending'
                        message = (
                            'Viewing updated successfully. '
                            'Your request will be reviewed by our team.'
                        )
                    else:
                        message = 'Viewing updated successfully.'

                viewing.save()

                return JsonResponse({
                    'status': 'success',
                    'message': message
                })

            return JsonResponse({
                'status': 'error',
                'errors': form.errors
            }, status=400)
        except Exception:
            return JsonResponse({
                'status': 'error',
                'message': 'An unexpected error occurred.'
            }, status=500)

    elif request.method == 'GET':
        slots = ViewingSlot.objects.filter(
            property=viewing.property,
            is_booked=False,
            date__gte=date.today()
        ).order_by('date', 'start_time')

        slots_data = [{
            'date': slot.date.strftime('%Y-%m-%d'),
            'start_time': slot.start_time.strftime('%H:%M'),
            'end_time': slot.end_time.strftime('%H:%M'),
        } for slot in slots]

        return JsonResponse({
            'slots': slots_data,
            'current_viewing': {
                'name': viewing.name,
                'contact': viewing.contact,
                'email': viewing.email,
                'message': viewing.message,
                'preferred_date': viewing.preferred_date.strftime('%Y-%m-%d'),
                'preferred_time': viewing.preferred_time.strftime('%H:%M'),
            }
        })

    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=405)


# View to delete a specific viewing appointment


@login_required
def delete_viewing(request, viewing_id):
    if request.method == 'POST':
        viewing = get_object_or_404(
            ViewingAppointment, id=viewing_id, user=request.user
        )
        viewing.delete()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'}, status=400)

# View to manage account settings


@login_required
def account_settings(request):
    user = request.user

    try:
        profile = user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=user)

    if request.method == 'POST':
        if 'update_profile' in request.POST:
            profile_form = ProfileUpdateForm(request.POST, instance=profile)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(
                    request, 'Your profile was successfully updated!'
                )
                return redirect('account_settings')
        elif 'change_password' in request.POST:
            password_form = ChangePasswordForm(user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(
                    request, 'Your password was successfully changed!'
                )
                return redirect('account_settings')
            else:
                messages.error(request, 'Please correct the error below.')
        elif 'delete_account' in request.POST:
            delete_form = DeleteAccountForm(request.POST)
            if delete_form.is_valid():
                user.delete()
                messages.success(
                    request, 'Your account was successfully deleted.'
                )
                return redirect('home')
    else:
        profile_form = ProfileUpdateForm(instance=profile)
        password_form = ChangePasswordForm(user)
        delete_form = DeleteAccountForm()

    return render(
        request, 'real_estate/account_settings.html', {
            'profile_form': profile_form,
            'password_form': password_form,
            'delete_form': delete_form,
        }
    )

# Class-based view to display the user's profile


class ProfileView(TemplateView):
    template_name = 'real_estate/profile.html'

# View to display the mortgage calculator


def mortgage_calculator(request):
    return render(request, 'real_estate/mortgage_calculator.html')

# View to display the list of property guides


def property_guides_list(request):
    return render(request, 'real_estate/property_guides_list.html')

# View to display the list of blog posts


def blog_list(request):
    return render(request, 'real_estate/blog_list.html')

# View to display homelessness advice


def homelessness_advice_list(request):
    return render(request, 'real_estate/homelessness_advice_list.html')

# View to display frequently asked questions (FAQ)


def faq_list(request):
    return render(request, 'real_estate/faq_list.html')
