from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django_summernote.fields import SummernoteTextField
from cloudinary.models import CloudinaryField


class FAQ(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='faq_posts')
    featured_image = CloudinaryField('image', default='placeholder')
    content = SummernoteTextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=[('draft', 'Draft'), ('published', 'Published')], default='draft')
    excerpt = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class Comment(models.Model):
    post = models.ForeignKey(FAQ, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=255)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'
