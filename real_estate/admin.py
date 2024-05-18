from django.contrib import admin
from .models import Property

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'property_type', 'price_display', 'location', 'transaction_type', 'bedrooms', 'bathrooms', 'garden', 'parking', 'pets_allowed', 'created_at')
    list_filter = ('property_type', 'transaction_type', 'furnished_type', 'garden', 'parking', 'pets_allowed', 'location')
    search_fields = ('title', 'description', 'location')