from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
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
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def paginate_properties(request, properties, per_page=20):
    page = request.GET.get('page', 1)
    paginator = Paginator(properties, per_page)  # Show 20 properties per page
    try:
        properties = paginator.page(page)
    except PageNotAnInteger:
        properties = paginator.page(1)
    except EmptyPage:
        properties = paginator.page(paginator.num_pages)
    return properties, paginator


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
            messages.success(request, 'Viewing appointment requested successfully.')
            return redirect('property_detail', slug=property.slug)
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    return JsonResponse({'status': 'error'}, status=400)


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


def property_sale(request):
    form = PropertySearchForm(request.GET or None)
    properties = Property.objects.filter(transaction_type='sale', publication_status='published')
    print("Initial properties count:", properties.count())

    if form.is_valid() and any(form.cleaned_data.values()):
        properties = filter_properties(form, properties)
        print("Filtered properties count:", properties.count())

    paginator = Paginator(properties, 20)
    page_number = request.GET.get('page')
    properties = paginator.get_page(page_number)

    print("Final properties in page:", len(properties))

    context = {
        'form': form,
        'properties': properties,
    }
    return render(request, 'real_estate/property_sale.html', context)


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
        'view_title': 'rent'
    }
    return render(request, 'real_estate/property_rent.html', context)


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
    }
    return render(request, 'real_estate/student_property.html', context)


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
    }
    return render(request, 'real_estate/view_land.html', context)


def property_detail(request, slug):
    property = get_object_or_404(Property, slug=slug)
    context = {
        'property': property,
        'additional_images': property.property_images.all(),
    }
    return render(request, 'real_estate/property_detail.html', context)


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
        favorite = FavoriteProperty.objects.filter(
            user=request.user, property=property
        ).first()
        if favorite:
            favorite.delete()
            return JsonResponse({'status': 'ok'})
        else:
            return JsonResponse({'status': 'not_found'}, status=404)
    return JsonResponse({'status': 'error'}, status=400)


@login_required
def schedule_viewing(request, slot_id):
    if request.method == 'POST':
        slot = get_object_or_404(ViewingSlot, id=slot_id, is_booked=False)
        ViewingAppointment.objects.create(
            slot=slot, user=request.user, property=slot.property
        )
        slot.is_booked = True
        slot.save()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'}, status=400)


@login_required
def view_property_slots(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    slots = ViewingSlot.objects.filter(
        property=property, is_booked=False
    ).order_by('date', 'start_time')
    context = {
        'property': property,
        'slots': slots
    }
    return render(request, 'real_estate/viewing_slots.html', context)


@login_required
def book_viewing_slot(request, slot_id):
    slot = get_object_or_404(ViewingSlot, id=slot_id)
    if request.method == 'POST':
        appointment = ViewingAppointment.objects.create(
            user=request.user,
            property=slot.property,
            slot=slot,
            name=request.POST.get('name', ''),
            contact=request.POST.get('contact', ''),
            email=request.POST.get('email', ''),
            preferred_date=slot.date,
            preferred_time=slot.start_time,
            viewing_decision='pending'
        )
        slot.is_booked = True
        slot.save()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'}, status=400)


@login_required
def view_pending_viewings(request):
    viewings = ViewingAppointment.objects.filter(user=request.user)
    context = {
        'viewings': viewings
    }
    return render(request, 'real_estate/pending_viewings.html', context)


@login_required
def update_viewing(request, viewing_id):
    viewing = get_object_or_404(
        ViewingAppointment, id=viewing_id, user=request.user
    )
    if request.method == 'POST':
        form = ViewingAppointmentForm(request.POST, instance=viewing)
        if form.is_valid():
            form.save()
            messages.success(request, 'Viewing updated successfully!')
            return redirect('view_pending_viewings')
    else:
        form = ViewingAppointmentForm(instance=viewing)
    return render(
        request, 'real_estate/update_viewing.html',
        {'form': form, 'viewing': viewing}
    )


@login_required
def delete_viewing(request, viewing_id):
    if request.method == 'POST':
        viewing = get_object_or_404(
            ViewingAppointment, id=viewing_id, user=request.user
        )
        viewing.delete()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'}, status=400)


@login_required
def account_settings(request):
    user = request.user

    try:
        profile = user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=user)

    profile_form = ProfileUpdateForm(instance=profile)
    password_form = ChangePasswordForm(user)
    delete_form = DeleteAccountForm()

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
            user.delete()
            messages.success(request, 'Your account was successfully deleted.')
            return redirect('home')

    return render(
        request, 'real_estate/account_settings.html', {
            'profile_form': profile_form,
            'password_form': password_form,
            'delete_form': delete_form,
        }
    )


class ProfileView(TemplateView):
    template_name = 'real_estate/profile.html'


def mortgage_calculator(request):
    return render(request, 'real_estate/mortgage_calculator.html')


def property_guides_list(request):
    return render(request, 'real_estate/property_guides_list.html')


def blog_list(request):
    return render(request, 'real_estate/blog_list.html')


def homelessness_advice_list(request):
    return render(request, 'real_estate/homelessness_advice_list.html')


def testimonials_list(request):
    return render(request, 'real_estate/testimonials_list.html')


def faq_list(request):
    return render(request, 'real_estate/faq_list.html')


def repairs(request):
    return render(request, 'real_estate/repairs.html')


def fire_safety(request):
    return render(request, 'real_estate/fire_safety.html')


def complaints(request):
    return render(request, 'real_estate/complaints.html')


def eviction(request):
    return render(request, 'real_estate/eviction.html')
