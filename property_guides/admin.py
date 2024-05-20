from django.contrib import admin
from .models import PropertyGuide

@admin.register(PropertyGuide)
class PropertyGuideAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)
