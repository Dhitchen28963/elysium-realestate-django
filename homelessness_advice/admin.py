from django.contrib import admin
from .models import Homeless, HomelessImage
from django_summernote.admin import SummernoteModelAdmin


"""
Defines an inline admin interface for adding and managing additional images
associated with a Homeless post. Displays one extra form by default.
"""


class HomelessImageInline(admin.TabularInline):
    model = HomelessImage
    extra = 1


"""
Customizes the Homeless model admin interface to include a rich-text editor
for content, fields for display, search functionality, slug prepopulation,
and an inline image management feature.
"""


class HomelessAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)
    list_display = ('title', 'slug', 'author', 'created_on', 'status')
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [HomelessImageInline]

# Registers the Homeless model with the customized admin interface.


admin.site.register(Homeless, HomelessAdmin)
