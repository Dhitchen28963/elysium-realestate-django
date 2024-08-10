from django.db import models
from cloudinary.models import CloudinaryField
from django_summernote.fields import SummernoteTextField
from django.contrib.auth.models import User
from .utils import clean_html_content

"""
Defines the Blog model with fields for title, slug, author, featured image,
rich-text content, timestamps, status, and an excerpt. It includes logic for
cleaning the content before saving.
"""


class Blog(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='blog_posts'
    )
    featured_image = CloudinaryField('image', default='placeholder')
    content = SummernoteTextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='draft'
    )
    excerpt = models.TextField(max_length=500, blank=True)

    def save(self, *args, **kwargs):
        self.content = clean_html_content(self.content)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


"""
Defines the Comment model with fields for the associated blog post, author,
comment body, timestamps, approval status, and pending approval status.
The body is cleaned before saving, and edited comments are marked not approved
and pending approval.
"""


class Comment(models.Model):
    post = models.ForeignKey(
        Blog, on_delete=models.CASCADE, related_name='comments'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='blog_comments'
    )
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    pending_approval = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.body = clean_html_content(self.body)
        if self.pk:
            self.approved = False
            self.pending_approval = True
        super(Comment, self).save(*args, **kwargs)

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'


"""
Defines the BlogImage model to handle additional images with blog post.
Each image is linked to a specific blog post and stored using Cloudinary.
"""


class BlogImage(models.Model):
    post = models.ForeignKey(
        Blog, on_delete=models.CASCADE, related_name='additional_images'
    )
    image = CloudinaryField('image')

    def __str__(self):
        return f"Image for {self.post.title}"
