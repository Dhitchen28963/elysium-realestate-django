from django import forms
from .models import Property, ViewingAppointment, Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from datetime import date

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

    def clean_preferred_date(self):
        preferred_date = self.cleaned_data['preferred_date']
        if preferred_date < date.today():
            raise forms.ValidationError("You cannot select a past date for viewing.")
        return preferred_date

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'email', 'address', 'telephone']

class ChangePasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control'})

class DeleteAccountForm(forms.Form):
    confirm_delete = forms.BooleanField(label='I confirm that I want to delete my account')