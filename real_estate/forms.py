from django import forms
from .models import Property, ViewingAppointment

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