from django.contrib import admin
from .models import Post, Comment, PostImage
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


class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_on', 'approved')
    list_filter = ('approved', 'created_on')
    search_fields = ['author', 'body']
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
