from django import forms
from .models import Property

class PropertySearchForm(forms.Form):
    search = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Search...'}))
    property_type = forms.ChoiceField(choices=[('', 'Any')] + Property.PROPERTY_TYPE_CHOICES, required=False)
    bedrooms_min = forms.IntegerField(required=False, min_value=0)
    bedrooms_max = forms.IntegerField(required=False, min_value=0)
    price_min = forms.IntegerField(required=False, min_value=0)
    price_max = forms.IntegerField(required=False, min_value=0)
    garden = forms.BooleanField(required=False)
    parking = forms.BooleanField(required=False)
    pets_allowed = forms.BooleanField(required=False)
    transaction_type = forms.ChoiceField(choices=[('sale', 'For Sale')], required=True)  # Add this line for sale page
