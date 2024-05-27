from django.contrib import admin
from .models import StudentProperty

class StudentPropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'property_type', 'price', 'status', 'created_on')
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(StudentProperty, StudentPropertyAdmin)
