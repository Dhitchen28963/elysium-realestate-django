from django.contrib import admin
from .models import Post, PropertyImage, Category
from django_summernote.admin import SummernoteModelAdmin

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

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)