from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from cloudinary.models import CloudinaryField
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django_summernote.fields import SummernoteTextField
from .utils import clean_html_content

"""
Function to get the default content type ID for the FAQ model.
Used as a default value for the content_type field in the Comment model.
"""


def get_default_faq_content_type_id():
    return ContentType.objects.get_for_model(FAQ).id


"""
Model representing a Frequently Asked Question (FAQ).
Includes fields for the title, slug, author, featured image, content,
creation and update timestamps, status, and an excerpt.
Automatically generates a slug from the title if not provided and
cleans the content before saving.
"""


class FAQ(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, null=True, blank=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='faq_posts'
    )
    featured_image = CloudinaryField('image', default='placeholder')
    content = SummernoteTextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=10,
        choices=[
            ('draft', 'Draft'),
            ('published', 'Published')
        ],
        default='draft'
    )
    excerpt = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.content = clean_html_content(self.content)
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


"""
Model representing a comment on a FAQ.
Includes fields for the associated FAQ post, author, comment body,
creation timestamp, approval status, and pending approval status.
It also supports content type identification for generic relations,
enabling comments to be associated with various content types.
"""


class Comment(models.Model):
    post = models.ForeignKey(
        'FAQ', on_delete=models.CASCADE, related_name='comments'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='faq_comments'
    )
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    pending_approval = models.BooleanField(default=False)
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE,
        related_name='faq_comment_set',
        default=get_default_faq_content_type_id
    )
    object_id = models.PositiveIntegerField(default=1)
    content_object = GenericForeignKey('content_type', 'object_id')

    def save(self, *args, **kwargs):
        self.body = clean_html_content(self.body)
        if self.pk:
            self.approved = False
            self.pending_approval = True
        super(Comment, self).save(*args, **kwargs)

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'


"""
Model representing additional images associated with a FAQ.
Each image is linked to a specific FAQ and stored using Cloudinary.
"""


class FAQImage(models.Model):
    faq = models.ForeignKey(
        FAQ, on_delete=models.CASCADE, related_name='additional_images'
    )
    image = CloudinaryField('image')

    def __str__(self):
        return f"Image for {self.faq.title}"
