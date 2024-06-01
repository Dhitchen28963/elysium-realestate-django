from django.contrib import admin
from .models import Property, ViewingSlot, FavoriteProperty, ViewingAppointment, PropertyMessage
from django_summernote.admin import SummernoteModelAdmin

@admin.register(Property)
class PropertyAdmin(SummernoteModelAdmin):
    list_display = ('title', 'slug', 'property_type', 'price_display', 'location', 'transaction_type', 'status', 'bedrooms', 'bathrooms', 'garden', 'parking', 'pets_allowed', 'created_at')
    list_filter = ('property_type', 'transaction_type', 'furnished_type', 'garden', 'parking', 'pets_allowed', 'location', 'status')
    search_fields = ('title', 'description', 'location')
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('description',)

@admin.register(ViewingSlot)
class ViewingSlotAdmin(admin.ModelAdmin):
    list_display = ('property', 'agent', 'date', 'start_time', 'end_time', 'is_booked')
    list_filter = ('property', 'agent', 'date', 'is_booked')
    search_fields = ('property__title', 'agent__username', 'date')

@admin.register(FavoriteProperty)
class FavoritePropertyAdmin(admin.ModelAdmin):
    list_display = ('user', 'property', 'added_on')
    list_filter = ('user', 'property', 'added_on')
    search_fields = ('user__username', 'property__title')

@admin.register(ViewingAppointment)
class ViewingAppointmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'property', 'name', 'email', 'preferred_date', 'preferred_time', 'viewing_decision', 'attended')
    list_filter = ('viewing_decision', 'attended', 'property', 'preferred_date')
    search_fields = ('user__username', 'property__title', 'name', 'email')
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
    list_display = ('property', 'user', 'name', 'email', 'message', 'created_on')
    list_filter = ('property', 'user', 'created_on')
    search_fields = ('property__title', 'user__username', 'name', 'email', 'message')
