from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            'title', 'slug', 'author', 'featured_image',
            'content', 'status', 'excerpt'
        )
