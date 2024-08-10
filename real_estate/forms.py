from django import forms
from .models import Property, ViewingAppointment, Profile
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from datetime import date

"""
Defines choices for the number of bedrooms, bathrooms, and price ranges,
including options for 'No Min' and 'No Max'.
"""
BEDROOMS_CHOICES = [(None, "No Min")] + [(i, i) for i in range(1, 11)] + [
    ("max", "No Max")
]
PRICE_CHOICES = [
    (None, "No Min")
] + [(i * 50000, f"£{i * 50000:,}") for i in range(1, 21)] + [
    (i * 250000, f"£{i * 250000:,}") for i in range(5, 9)
] + [(i * 1000000, f"£{i * 1000000:,}") for i in range(2, 11)] + [
    ("max", "No Max")
]
BATHROOMS_CHOICES = [(None, "No Min")] + [(i, i) for i in range(1, 11)] + [
    ("max", "No Max")
]

"""
Form for searching properties based on various criteria like location,
property type, number of bedrooms, bathrooms, price range, and amenities.
"""


class PropertySearchForm(forms.Form):
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Enter location'})
    )
    location = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Enter location'})
    )
    property_type = forms.ChoiceField(
        choices=[('any', 'Any')] + list(Property.PROPERTY_TYPE_CHOICES),
        required=False
    )
    bedrooms_min = forms.ChoiceField(
        choices=BEDROOMS_CHOICES, required=False, initial=None
    )
    bedrooms_max = forms.ChoiceField(
        choices=BEDROOMS_CHOICES, required=False, initial="max"
    )
    price_min = forms.ChoiceField(
        choices=PRICE_CHOICES, required=False, initial=None
    )
    price_max = forms.ChoiceField(
        choices=PRICE_CHOICES, required=False, initial="max"
    )
    bathrooms_min = forms.ChoiceField(
        choices=BATHROOMS_CHOICES, required=False, initial=None
    )
    bathrooms_max = forms.ChoiceField(
        choices=BATHROOMS_CHOICES, required=False, initial="max"
    )
    garden = forms.BooleanField(required=False)
    parking = forms.BooleanField(required=False)
    pets_allowed = forms.BooleanField(required=False)

    def clean_bedrooms_min(self):
        """
        Cleans the minimum bedrooms field, returning None if not specified.
        """
        data = self.cleaned_data['bedrooms_min']
        return None if data in [None, ''] else data

    def clean_bedrooms_max(self):
        """
        Cleans the maximum bedrooms field, returning None if 'max' is selected.
        """
        data = self.cleaned_data['bedrooms_max']
        return None if data in [None, "max"] else data

    def clean_price_min(self):
        """
        Cleans the minimum price field, returning None if it's not specified.
        """
        data = self.cleaned_data['price_min']
        return None if data in [None, ''] else data

    def clean_price_max(self):
        """
        Cleans the maximum price field, returning None if 'max' is selected.
        """
        data = self.cleaned_data['price_max']
        return None if data in [None, "max"] else data

    def clean_bathrooms_min(self):
        """
        Cleans the minimum bathrooms field, returning None if not specified.
        """
        data = self.cleaned_data['bathrooms_min']
        return None if data in [None, ''] else data

    def clean_bathrooms_max(self):
        """
        Cleans the maximum bathrooms field, returning None if 'max' selected.
        """
        data = self.cleaned_data['bathrooms_max']
        return None if data in [None, "max"] else data


"""
Form for scheduling a viewing appointment for a property.
Includes validation to ensure the preferred date is not in the past.
"""


class ViewingAppointmentForm(forms.ModelForm):
    class Meta:
        model = ViewingAppointment
        fields = [
            'name',
            'contact',
            'email',
            'preferred_date',
            'preferred_time',
            'message'
        ]

    def clean_preferred_date(self):
        preferred_date = self.cleaned_data['preferred_date']
        if preferred_date < date.today():
            raise forms.ValidationError(
                "You cannot select a past date for viewing."
            )
        return preferred_date


"""
Form for updating user profile information such as name, email,
address, and telephone.
"""


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'email', 'address', 'telephone']


"""
Custom form for changing a user's password, with styled input fields.
"""


class ChangePasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update(
            {'class': 'form-control'}
        )
        self.fields['new_password1'].widget.attrs.update(
            {'class': 'form-control'}
        )
        self.fields['new_password2'].widget.attrs.update(
            {'class': 'form-control'}
        )


"""
Form for confirming account deletion, requiring the user to
check a confirmation box.
"""


class DeleteAccountForm(forms.Form):
    confirm_delete = forms.BooleanField(
        label='I confirm that I want to delete my account'
    )
