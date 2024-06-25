from django import forms
from .models import StudentProperty, PROPERTY_TYPES, ViewingAppointment, SavedSearch

class StudentPropertyForm(forms.Form):
    search = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Enter location'}))
    property_type = forms.ChoiceField(choices=[('', 'Any')] + PROPERTY_TYPES, required=False)
    bedrooms_min = forms.IntegerField(required=False)
    bedrooms_max = forms.IntegerField(required=False)
    price_min = forms.DecimalField(required=False)
    price_max = forms.DecimalField(required=False)
    garden = forms.BooleanField(required=False)
    parking = forms.BooleanField(required=False)
    pets_allowed = forms.BooleanField(required=False)

class ViewingAppointmentForm(forms.ModelForm):
    class Meta:
        model = ViewingAppointment
        fields = ['name', 'contact', 'email', 'message', 'preferred_date', 'preferred_time']

class SavedSearchForm(forms.ModelForm):
    class Meta:
        model = SavedSearch
        fields = [
            'search_name', 'location', 'property_type', 'bedrooms_min', 'bedrooms_max',
            'bathrooms_min', 'bathrooms_max', 'price_min', 'price_max', 'garden', 'parking',
            'pets_allowed', 'furnished_type'
        ]