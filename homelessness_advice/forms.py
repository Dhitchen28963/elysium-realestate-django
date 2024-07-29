from django import forms
from .models import Homeless


class HomelessForm(forms.ModelForm):
    class Meta:
        model = Homeless
        fields = (
            'title', 'slug', 'author', 'featured_image',
            'content', 'status', 'excerpt'
        )
