from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Post, PropertyImage, Category
from django.utils.html import escape, mark_safe

class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1

class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)
    list_display = ('title', 'category', 'created_on', 'updated_on')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    fields = ('title', 'slug', 'category', 'featured_image', 'content')
    inlines = [PropertyImageInline]

    def save_model(self, request, obj, form, change):
        obj.content = mark_safe(obj.content)
        super().save_model(request, obj, form, change)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
