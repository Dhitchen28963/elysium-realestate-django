from django import forms
from .models import StudentProperty

class StudentPropertyForm(forms.ModelForm):
    class Meta:
        model = StudentProperty
        fields = ('title', 'slug', 'description', 'property_type', 'price', 'furnished_type', 'location', 'bedrooms', 'bathrooms', 'garden', 'parking', 'pets_allowed', 'property_image', 'floor_plan', 'energy_efficiency_rating', 'status')
