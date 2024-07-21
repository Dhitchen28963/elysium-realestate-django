from django.contrib import admin
from .models import FAQ, Comment, FAQImage
from django_summernote.admin import SummernoteModelAdmin


class FAQImageInline(admin.TabularInline):
    model = FAQImage
    extra = 1  # Number of extra forms to display in the admin


class FAQAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)
    list_display = ('title', 'slug', 'author', 'created_on', 'status')
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [FAQImageInline]


class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_on', 'approved')
    list_filter = ('approved', 'created_on')
    search_fields = ['author', 'body']
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)


admin.site.register(FAQ, FAQAdmin)
admin.site.register(Comment, CommentAdmin)
