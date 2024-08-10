from django import forms
from .models import Post
from django_summernote.widgets import SummernoteWidget

"""
Defines a form for creating and updating Post instances.
Utilizes a rich-text editor for the content field through the SummernoteWidget.
"""


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'slug', 'featured_image', 'content')
        widgets = {
            'content': SummernoteWidget(),
        }
