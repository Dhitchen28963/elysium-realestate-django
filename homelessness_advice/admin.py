from django.contrib import admin
from .models import Homeless, HomelessImage
from django_summernote.admin import SummernoteModelAdmin


class HomelessImageInline(admin.TabularInline):
    model = HomelessImage
    extra = 1


class HomelessAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)
    list_display = ('title', 'slug', 'author', 'created_on', 'status')
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [HomelessImageInline]


admin.site.register(Homeless, HomelessAdmin)
