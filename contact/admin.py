from django.contrib import admin
from .models import ContactMessage

"""
Customizes the ContactMessage model admin interface by defining the fields
to display in the list view and the fields available for search.
"""


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email')
