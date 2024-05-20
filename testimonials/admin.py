from django.contrib import admin
from .models import Testimonial

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('author', 'created_at')
    search_fields = ('author',)
    list_filter = ('created_at',)
    ordering = ('-created_at',)
