from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Post, PropertyImage, Category
from django.utils.html import escape, mark_safe

"""
Defines an inline admin interface for the PropertyImage model.
Allows managing related PropertyImage instances directly with Post admin form.
"""


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1


"""
Customizes the Post model admin interface.
Includes fields with a rich-text editor, list fields for display,
search fields, fields to prepopulate, and an inline image management feature.
"""


class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)
    list_display = ('title', 'category', 'created_on', 'updated_on')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    fields = ('title', 'slug', 'category', 'featured_image', 'content')
    inlines = [PropertyImageInline]

    def save_model(self, request, obj, form, change):
        """
        Customizes the save behavior for the Post model.
        Marks content as safe HTML before saving to ensure correct rendering
        """
        obj.content = mark_safe(obj.content)
        super().save_model(request, obj, form, change)


"""
Customizes the Category model admin interface.
Allows for the management of categories with display and search capabilities.
"""


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Register the Post and Category models with their respective admin classes


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
