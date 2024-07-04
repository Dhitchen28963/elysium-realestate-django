from django.contrib import admin
from .models import Post
from django_summernote.admin import SummernoteModelAdmin

class PostAdmin(admin.ModelAdmin):
    summernote_fields = ('content',)
    list_display = ('title', 'slug', 'author', 'created_on', 'status')
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Post, PostAdmin)
