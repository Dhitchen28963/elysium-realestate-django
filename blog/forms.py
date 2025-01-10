from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Comment

"""
Creates a form for submitting comments, includes configuration for
Crispy Forms, and overrides the save method to ensure that new or edited
comments are marked as not approved by default.
"""


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'placeholder': 'Enter a comment'}),
        }

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['body'].label = ''
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))

    def save(self, commit=True):
        comment = super().save(commit=False)
        # Mark comment as not approved when created or edited
        comment.approved = False
        if commit:
            comment.save()
        return comment
