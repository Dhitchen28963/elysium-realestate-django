from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.http import JsonResponse
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView, DetailView
from .forms import StudentPropertyForm, ViewingAppointmentForm, SavedSearchForm
from .models import StudentProperty, StudentPropertyMessage, ViewingSlot, ViewingAppointment, SavedSearch, PropertyAlert, FavoriteProperty

class StudentPropertyList(ListView):
    model = StudentProperty
    template_name = 'student_accommodation/student_property.html'
    context_object_name = 'properties'

    def get_queryset(self):
        queryset = super().get_queryset()
        form = StudentPropertyForm(self.request.GET)
        if form.is_valid():
            if form.cleaned_data.get('search'):
                queryset = queryset.filter(location__icontains=form.cleaned_data['search'])
            if form.cleaned_data.get('location'):
                queryset = queryset.filter(location__icontains=form.cleaned_data['location'])
            if form.cleaned_data.get('property_type') and form.cleaned_data['property_type'] != 'any':
                queryset = queryset.filter(property_type=form.cleaned_data['property_type'])
            if form.cleaned_data.get('bedrooms_min'):
                queryset = queryset.filter(bedrooms__gte=form.cleaned_data['bedrooms_min'])
            if form.cleaned_data.get('bedrooms_max'):
                queryset = queryset.filter(bedrooms__lte=form.cleaned_data['bedrooms_max'])
            if form.cleaned_data.get('price_min'):
                queryset = queryset.filter(price__gte=form.cleaned_data['price_min'])
            if form.cleaned_data.get('price_max'):
                queryset = queryset.filter(price__lte=form.cleaned_data['price_max'])
            if form.cleaned_data.get('garden'):
                queryset = queryset.filter(garden=form.cleaned_data['garden'])
            if form.cleaned_data.get('parking'):
                queryset = queryset.filter(parking=form.cleaned_data['parking'])
            if form.cleaned_data.get('pets_allowed'):
                queryset = queryset.filter(pets_allowed=form.cleaned_data['pets_allowed'])
        return queryset

class StudentPropertyDetail(DetailView):
    model = StudentProperty
    template_name = 'student_accommodation/student_property_detail.html'
    context_object_name = 'property'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['additional_images'] = self.object.property_images.all()
        context['viewing_slots'] = self.object.viewing_slots.all()
        return context

def student_property_rent(request):
    form = StudentPropertyForm(request.GET)
    properties = StudentProperty.objects.filter(publication_status='published')

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
    return render(request, 'student_accommodation/student_property.html', context)

@login_required
def add_student_property_to_favorites(request, property_id):
    if request.method == 'POST':
        property = get_object_or_404(StudentProperty, id=property_id)
        favorite, created = FavoriteProperty.objects.get_or_create(user=request.user, property=property)
        if created:
            return JsonResponse({'status': 'ok'})
        else:
            return JsonResponse({'status': 'exists'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def view_student_favorites(request):
    favorites = FavoriteProperty.objects.filter(user=request.user)
    context = {
        'favorites': favorites
    }
    return render(request, 'student_accommodation/favorites.html', context)

@login_required
def remove_student_property_from_favorites(request, property_id):
    if request.method == 'POST':
        property = get_object_or_404(StudentProperty, id=property_id)
        favorite = FavoriteProperty.objects.filter(user=request.user, property=property).first()
        if favorite:
            favorite.delete()
            return JsonResponse({'status': 'ok'})
        else:
            return JsonResponse({'status': 'not_found'}, status=404)
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def contact_student_property(request, property_id):
    if request.method == 'POST':
        property = get_object_or_404(StudentProperty, id=property_id)
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        StudentPropertyMessage.objects.create(
            property=property,
            user=request.user,
            agent=property.agent,
            name=name,
            email=email,
            message=message
        )
        return JsonResponse({'status': 'message sent'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def schedule_student_viewing(request):
    if request.method == 'POST':
        slot_id = request.POST.get('slot_id')
        slot = get_object_or_404(ViewingSlot, id=slot_id, is_booked=False)
        ViewingAppointment.objects.create(slot=slot, user=request.user, property=slot.property)
        slot.is_booked = True
        slot.save()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'}, status=400)


@login_required
def view_student_property_slots(request, property_id):
    property = get_object_or_404(StudentProperty, id=property_id)
    slots = ViewingSlot.objects.filter(property=property, is_booked=False).order_by('date', 'start_time')
    context = {
        'property': property,
        'slots': slots
    }
    return render(request, 'student_accommodation/viewing_slots.html', context)

@login_required
def view_pending_student_viewings(request):
    pending_viewings = ViewingAppointment.objects.filter(user=request.user, is_scheduled=False)
    return render(request, 'student_accommodation/pending_viewings.html', {'pending_viewings': pending_viewings})

@login_required
def view_scheduled_student_viewings(request):
    scheduled_viewings = ViewingAppointment.objects.filter(user=request.user, viewing_decision='accepted')
    context = {
        'scheduled_viewings': scheduled_viewings
    }
    return render(request, 'student_accommodation/scheduled_viewings.html', context)

@login_required
def save_student_search(request):
    if request.method == 'POST':
        form = SavedSearchForm(request.POST)
        if form.is_valid():
            saved_search = form.save(commit=False)
            saved_search.user = request.user
            saved_search.save()
            return redirect('view_student_saved_searches')
    else:
        form = SavedSearchForm()
    return render(request, 'student_accommodation/save_search.html', {'form': form})

@login_required
def view_student_saved_searches(request):
    saved_searches = SavedSearch.objects.filter(user=request.user)
    return render(request, 'student_accommodation/saved_searches.html', {'saved_searches': saved_searches})

@login_required
def view_student_property_alerts(request):
    alerts = PropertyAlert.objects.filter(user=request.user, seen=False)
    return render(request, 'student_accommodation/property_alerts.html', {'alerts': alerts})

@login_required
def request_student_custom_viewing(request, property_id):
    property = get_object_or_404(StudentProperty, id=property_id)

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
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def accept_student_appointment(request, appointment_id):
    appointment = get_object_or_404(ViewingAppointment, id=appointment_id)
    if request.method == 'POST':
        appointment.viewing_decision = 'accepted'
        appointment.save()

        send_mail(
            'Your Viewing Appointment is Accepted',
            f'Dear {appointment.user.username}, your viewing appointment for {appointment.property.title} has been accepted.',
            'from@example.com',
            [appointment.user.email],
            fail_silently=False,
        )

        messages.success(request, 'The appointment has been accepted and the user has been notified.')
        return redirect('view_pending_student_viewings')

    context = {
        'appointment': appointment,
    }
    return render(request, 'student_accommodation/accept_appointment.html', context)

class StudentProfileView(TemplateView):
    template_name = 'student_accommodation/profile.html'

class StudentMessagesView(TemplateView):
    template_name = 'student_accommodation/messages.html'

class StudentAccountSettingsView(TemplateView):
    template_name = 'student_accommodation/account_settings.html'
