from django.contrib import admin
from .models import StudentProperty, FavoriteProperty, StudentPropertyMessage, ViewingSlot, ViewingAppointment, SavedSearch, PropertyAlert
from django_summernote.admin import SummernoteModelAdmin

class StudentPropertyAdmin(SummernoteModelAdmin):
    summernote_fields = ('description',)  # Specify the fields you want to use Summernote with
    list_display = ('title', 'location', 'price', 'property_type', 'publication_status')
    search_fields = ('title', 'location')
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(StudentProperty, StudentPropertyAdmin)
admin.site.register(FavoriteProperty)
admin.site.register(StudentPropertyMessage)
admin.site.register(ViewingSlot)
admin.site.register(ViewingAppointment)
admin.site.register(SavedSearch)
admin.site.register(PropertyAlert)