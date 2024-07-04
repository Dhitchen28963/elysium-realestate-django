from django import forms
from .models import Post
from django_summernote.widgets import SummernoteWidget

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'slug', 'featured_image', 'content')
        widgets = {
            'content': SummernoteWidget(),
        }