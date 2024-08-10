from django.contrib import admin
from .models import FAQ, Comment, FAQImage
from django_summernote.admin import SummernoteModelAdmin

"""
Defines an inline admin interface for managing FAQ images directly within
the FAQ admin page. Includes a single extra form by default.
"""


class FAQImageInline(admin.TabularInline):
    model = FAQImage
    extra = 1  # Number of extra forms to display in the admin


"""
Customizes FAQ model admin interface to include fields with rich-text editor,
list fields for display, search fields, fields to prepopulate, & inline image
management feature.
"""


class FAQAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)
    list_display = ('title', 'slug', 'author', 'created_on', 'status')
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [FAQImageInline]


"""
Customizes the Comment model admin interface to display specific fields,
filter comments based on approval status and creation date, search through
comments, and provide an action to approve multiple comments at once.
"""


class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_on', 'approved')
    list_filter = ('approved', 'created_on')
    search_fields = ['author', 'body']
    actions = ['approve_comments']

    """
    Custom action to approve selected comments in the admin interface.
    """
    def approve_comments(self, request, queryset):
        queryset.update(approved=True)


# Registering the models with the admin site
admin.site.register(FAQ, FAQAdmin)
admin.site.register(Comment, CommentAdmin)
