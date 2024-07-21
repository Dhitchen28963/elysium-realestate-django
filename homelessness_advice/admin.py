from django.contrib import admin
from .models import Post, PostImage
from django_summernote.admin import SummernoteModelAdmin


class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 1


class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)
    list_display = ('title', 'slug', 'author', 'created_on', 'status')
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [PostImageInline]


admin.site.register(Post, PostAdmin)
