from django import forms
from .models import StudentProperty, ViewingAppointment, SavedSearch

class StudentPropertyForm(forms.ModelForm):
    class Meta:
        model = StudentProperty
        fields = ['title', 'slug', 'description', 'property_type', 'price', 'furnished_type', 'location', 'bedrooms', 'bathrooms', 'garden', 'parking', 'pets_allowed', 'property_image', 'floor_plan', 'energy_efficiency_rating', 'availability_status', 'publication_status']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class ViewingAppointmentForm(forms.ModelForm):
    class Meta:
        model = ViewingAppointment
        fields = ['name', 'contact', 'email', 'message', 'preferred_date', 'preferred_time']

class SavedSearchForm(forms.ModelForm):
    class Meta:
        model = SavedSearch
        fields = ['search_name', 'location', 'property_type', 'bedrooms_min', 'bedrooms_max', 'bathrooms_min', 'bathrooms_max', 'price_min', 'price_max', 'garden', 'parking', 'pets_allowed', 'furnished_type']
