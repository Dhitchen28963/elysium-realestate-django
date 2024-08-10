from django.contrib import admin
from .models import Blog, Comment, BlogImage
from django_summernote.admin import SummernoteModelAdmin

"""
Defines an inline model for adding and managing images related to blog posts
within the blog admin interface.
"""
class BlogImageInline(admin.TabularInline):
    model = BlogImage
    extra = 1

"""
Customizes the Blog model admin interface to include fields with a rich-text editor,
list fields for display, search fields, fields to prepopulate, and an inline image
management feature.
"""
class BlogAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)
    list_display = ('title', 'slug', 'author', 'created_on', 'status')
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [BlogImageInline]

"""
Customizes the Comment model admin interface to include list fields, filters, 
and search functionality.
"""
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_on', 'approved')
    list_filter = ('approved', 'created_on')
    search_fields = ['author', 'body']

"""
Registers the Blog and Comment models with the custom admin interfaces.
"""
admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment, CommentAdmin)
