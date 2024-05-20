from django.contrib import admin
from .models import StudentAccommodation

@admin.register(StudentAccommodation)
class StudentAccommodationAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)
