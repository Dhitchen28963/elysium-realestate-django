from django import forms
from .models import ContactMessage

"""
Defines the ContactForm for creating and editing contact messages. This form
is based on the ContactMessage model and includes fields for the name, email,
and message, with a custom widget for the message field.
"""


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),
        }
