from django import forms
from .models import Property, ViewingAppointment, SavedSearch

class PropertySearchForm(forms.Form):
    search = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Enter location'}))
    location = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Enter location'}))
    property_type = forms.ChoiceField(choices=[('any', 'Any')] + list(Property.PROPERTY_TYPE_CHOICES), required=False)
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
        fields = ['name', 'contact', 'email', 'preferred_date', 'preferred_time', 'message']

class SavedSearchForm(forms.ModelForm):
    class Meta:
        model = SavedSearch
        fields = [
            'search_name', 'location', 'property_type', 'bedrooms_min', 'bedrooms_max',
            'bathrooms_min', 'bathrooms_max', 'price_min', 'price_max', 'garden', 'parking',
            'pets_allowed', 'furnished_type'
        ]
        widgets = {
            'property_type': forms.Select(choices=[
                ('detached-houses', 'Detached houses'),
                ('semi-detached-houses', 'Semi-detached houses'),
                ('terraced-houses', 'Terraced houses'),
                ('mobile-park-homes', 'Mobile / Park homes'),
                ('boats', 'Boats'),
                ('flats-apartments', 'Flats / Apartments'),
                ('bungalows', 'Bungalows'),
                ('land', 'Land'),
                ('commercial-property', 'Commercial Property'),
                ('hmo', 'HMO\'s')
            ]),
            'price_min': forms.NumberInput(),
            'price_max': forms.NumberInput(),
        }