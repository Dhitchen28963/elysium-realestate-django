from django import forms
from .models import Homeless

"""
Defines a ModelForm for the Homeless model, specifying the fields that should
be included in the form: title, slug, author, featured image, content, status,
and excerpt.
"""
class HomelessForm(forms.ModelForm):
    class Meta:
        model = Homeless
        fields = (
            'title', 'slug', 'author', 'featured_image',
            'content', 'status', 'excerpt'
        )
