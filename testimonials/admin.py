from django.contrib import admin
from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')
    search_fields = ['title', 'comment']


admin.site.register(Post, PostAdmin)
