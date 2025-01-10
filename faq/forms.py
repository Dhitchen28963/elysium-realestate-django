from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Comment

"""
Form class for handling comment creation and editing.
Utilizes Django's ModelForm for automatic field creation for Comment model.
Includes a helper for Crispy Forms to handle form rendering & submissions.
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
        self.fields['body'].label = ''  # Remove the label
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))

    """
    Overrides the save method to automatically mark the comment as not approved
    whenever it is created or edited.
    """
    def save(self, commit=True):
        comment = super().save(commit=False)
        # Mark comment as not approved when created or edited
        comment.approved = False
        if commit:
            comment.save()
        return comment
