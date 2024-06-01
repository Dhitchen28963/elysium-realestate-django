from django.contrib import admin
from .models import StudentProperty
from django_summernote.admin import SummernoteModelAdmin

@admin.register(StudentProperty)
class StudentPropertyAdmin(SummernoteModelAdmin):
    list_display = ('title', 'slug', 'property_type', 'price', 'status', 'created_on')
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('description',)