from django.contrib import admin
from .models import Testimonial

class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('author', 'body', 'created_on')
    search_fields = ('author', 'body')

admin.site.register(Testimonial, TestimonialAdmin)
