from django.contrib import admin
from .models import HomelessnessAdvice

@admin.register(HomelessnessAdvice)
class HomelessnessAdviceAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)
