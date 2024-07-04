from django.contrib import admin
from .models import Property, PropertyImage, ViewingSlot, FavoriteProperty, ViewingAppointment, PropertyMessage, SavedSearch, PropertyAlert
from django_summernote.admin import SummernoteModelAdmin

class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1

@admin.register(Property)
class PropertyAdmin(SummernoteModelAdmin):
    list_display = ('title', 'slug', 'property_type', 'price_display', 'location', 'transaction_type', 'publication_status', 'availability_status', 'bedrooms', 'bathrooms', 'garden', 'parking', 'pets_allowed', 'created_at')
    list_filter = ('property_type', 'transaction_type', 'furnished_type', 'garden', 'parking', 'pets_allowed', 'location', 'publication_status', 'availability_status')
    search_fields = ('title', 'description', 'location')
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('description',)
    inlines = [PropertyImageInline]

@admin.register(SavedSearch)
class SavedSearchAdmin(admin.ModelAdmin):
    list_display = ('user', 'search_name', 'location', 'property_type', 'bedrooms_min', 'bedrooms_max', 'price_min', 'price_max', 'furnished_type', 'created_at')
    search_fields = ('user__username', 'search_name', 'location', 'property_type')

@admin.register(PropertyAlert)
class PropertyAlertAdmin(admin.ModelAdmin):
    list_display = ('user', 'property', 'created_at', 'seen')
    search_fields = ('user__username', 'property__title')

@admin.register(ViewingSlot)
class ViewingSlotAdmin(admin.ModelAdmin):
    list_display = ('get_property_title', 'get_agent_username', 'date', 'start_time', 'end_time', 'is_booked')
    list_filter = ('date', 'is_booked')
    search_fields = ('property__title', 'agent__username', 'date')

    def get_property_title(self, obj):
        return obj.property.title
    get_property_title.admin_order_field = 'property'
    get_property_title.short_description = 'Property'

    def get_agent_username(self, obj):
        return obj.agent.username
    get_agent_username.admin_order_field = 'agent'
    get_agent_username.short_description = 'Agent'

@admin.register(FavoriteProperty)
class FavoritePropertyAdmin(admin.ModelAdmin):
    list_display = ('user', 'property', 'added_on')
    list_filter = ('user', 'property', 'added_on')
    search_fields = ('user__username', 'property__title')

@admin.register(ViewingAppointment)
class ViewingAppointmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'property', 'name', 'email', 'preferred_date', 'preferred_time', 'viewing_decision', 'attended', 'agent_name', 'agent_contact', 'agent_email')
    list_filter = ('viewing_decision', 'attended', 'preferred_date')
    search_fields = ('user__username', 'property__title', 'name', 'email', 'agent_name', 'agent_contact', 'agent_email')
    actions = ['mark_as_attended', 'mark_as_not_attended', 'accept_viewing', 'reject_viewing']

    def mark_as_attended(self, request, queryset):
        queryset.update(attended=True)
    mark_as_attended.short_description = "Mark selected appointments as attended"

    def mark_as_not_attended(self, request, queryset):
        queryset.update(attended=False)
    mark_as_not_attended.short_description = "Mark selected appointments as not attended"

    def accept_viewing(self, request, queryset):
        queryset.update(viewing_decision='accepted')
    accept_viewing.short_description = "Accept selected viewing requests"

    def reject_viewing(self, request, queryset):
        queryset.update(viewing_decision='rejected')
    reject_viewing.short_description = "Reject selected viewing requests"

@admin.register(PropertyMessage)
class PropertyMessageAdmin(admin.ModelAdmin):
    list_display = ('get_property_title', 'get_user_username', 'name', 'email', 'message', 'created_on')
    list_filter = ('property', 'created_on')
    search_fields = ('property__title', 'user__username', 'name', 'email', 'message')

    def get_property_title(self, obj):
        return obj.property.title
    get_property_title.admin_order_field = 'property'
    get_property_title.short_description = 'Property'

    def get_user_username(self, obj):
        return obj.user.username
    get_user_username.admin_order_field = 'user'
    get_user_username.short_description = 'User'