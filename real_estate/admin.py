from django.contrib import admin
from .models import Property
from django_summernote.admin import SummernoteModelAdmin

@admin.register(Property)
class PropertyAdmin(SummernoteModelAdmin):
    list_display = ('title', 'property_type', 'price_display', 'location', 'transaction_type', 'status', 'bedrooms', 'bathrooms', 'garden', 'parking', 'pets_allowed', 'created_at')
    list_filter = ('property_type', 'transaction_type', 'furnished_type', 'garden', 'parking', 'pets_allowed', 'location', 'status')
    search_fields = ('title', 'description', 'location')
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('description',)
