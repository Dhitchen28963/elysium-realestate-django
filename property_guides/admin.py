from django.contrib import admin
from .models import Post, Category
from django_summernote.admin import SummernoteModelAdmin

class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)
    list_display = ('title', 'category', 'created_on', 'updated_on')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    fields = ('title', 'slug', 'category', 'featured_image', 'content')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)