from django.contrib import admin
from .models import (
    Property, PropertyImage, ViewingSlot, FavoriteProperty, ViewingAppointment
)
from django_summernote.admin import SummernoteModelAdmin

"""
Inline model for managing property images in the admin interface.
Allows adding multiple images directly from the property admin page.
"""


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1


"""
Admin configuration for the Property model.
Includes features such as rich-text editing for descriptions,
prepopulated slug fields, and inline image management.
"""


@admin.register(Property)
class PropertyAdmin(SummernoteModelAdmin):
    list_display = (
        'title', 'slug', 'property_type', 'price_display', 'location',
        'transaction_type', 'publication_status', 'availability_status',
        'bedrooms', 'bathrooms', 'garden', 'parking', 'pets_allowed',
        'created_at'
    )
    list_filter = (
        'property_type', 'transaction_type', 'furnished_type', 'garden',
        'parking', 'pets_allowed', 'location', 'publication_status',
        'availability_status'
    )
    search_fields = ('title', 'description', 'location')
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('description',)
    inlines = [PropertyImageInline]


"""
Admin configuration for the ViewingSlot model.
Includes custom display functions for associated property and agent details,
as well as filtering and searching capabilities.
"""


@admin.register(ViewingSlot)
class ViewingSlotAdmin(admin.ModelAdmin):
    list_display = (
        'get_property_title', 'get_agent_username', 'date', 'start_time',
        'end_time', 'is_booked'
    )
    list_filter = ('date', 'is_booked')
    search_fields = ('property__title', 'agent__username', 'date')

    def get_property_title(self, obj):
        """
        Returns the title of the property associated with the viewing slot.
        """
        if obj.property:
            return obj.property.title
        return "No Property"
    get_property_title.admin_order_field = 'property__title'
    get_property_title.short_description = 'Property'

    def get_agent_username(self, obj):
        """
        Returns the username of the agent associated with the viewing slot.
        """
        return obj.agent.username if obj.agent else "No Agent"
    get_agent_username.admin_order_field = 'agent__username'
    get_agent_username.short_description = 'Agent'


"""
Admin configuration for the FavoriteProperty model.
Allows filtering and searching by user and property, with a display of
when each favorite was added.
"""


@admin.register(FavoriteProperty)
class FavoritePropertyAdmin(admin.ModelAdmin):
    list_display = ('user', 'property', 'added_on')
    list_filter = ('user', 'property', 'added_on')
    search_fields = ('user__username', 'property__title')


"""
Admin configuration for the ViewingAppointment model.
Includes custom actions for marking attendance and accepting or rejecting
viewing requests, as well as filtering and searching options.
"""


@admin.register(ViewingAppointment)
class ViewingAppointmentAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'property', 'name', 'email', 'preferred_date',
        'preferred_time', 'viewing_decision', 'attended', 'agent_name',
        'agent_contact', 'agent_email'
    )
    list_filter = ('viewing_decision', 'attended', 'preferred_date')
    search_fields = (
        'user__username', 'property__title', 'name', 'email', 'agent_name',
        'agent_contact', 'agent_email'
    )
    actions = [
        'mark_as_attended', 'mark_as_not_attended', 'accept_viewing',
        'reject_viewing'
    ]

    def mark_as_attended(self, request, queryset):
        """
        Marks selected viewing appointments as attended.
        """
        queryset.update(attended=True)

    mark_as_attended.short_description = (
        "Mark selected appointments as attended"
    )

    def mark_as_not_attended(self, request, queryset):
        """
        Marks selected viewing appointments as not attended.
        """
        queryset.update(attended=False)

    mark_as_not_attended.short_description = (
        "Mark selected appointments as not attended"
    )

    def accept_viewing(self, request, queryset):
        """
        Marks selected viewing requests as accepted.
        """
        queryset.update(viewing_decision='accepted')

    accept_viewing.short_description = "Accept selected viewing requests"

    def reject_viewing(self, request, queryset):
        """
        Marks selected viewing requests as rejected.
        """
        queryset.update(viewing_decision='rejected')

    reject_viewing.short_description = "Reject selected viewing requests"
