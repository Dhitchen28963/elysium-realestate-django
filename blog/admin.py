from django.contrib import admin
from .models import Blog, Comment, BlogImage
from django_summernote.admin import SummernoteModelAdmin


class BlogImageInline(admin.TabularInline):
    model = BlogImage
    extra = 1


class BlogAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)
    list_display = ('title', 'slug', 'author', 'created_on', 'status')
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [BlogImageInline]


class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_on', 'approved')
    list_filter = ('approved', 'created_on')
    search_fields = ['author', 'body']

admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment, CommentAdmin)
