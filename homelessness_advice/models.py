from django.db import models
from django.contrib.auth.models import User
from django_summernote.fields import SummernoteTextField
from cloudinary.models import CloudinaryField
from .utils import clean_html_content

class Homeless(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='homelessness_advice_posts'
    )
    featured_image = CloudinaryField('image', default='placeholder')
    content = SummernoteTextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES,
        default='draft'
    )
    excerpt = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.content = clean_html_content(self.content)
        super().save(*args, **kwargs)


class HomelessImage(models.Model):
    homeless = models.ForeignKey(
        Homeless, on_delete=models.CASCADE,
        related_name='additional_images'
    )
    image = CloudinaryField('image')

    def __str__(self):
        return f"Image for {self.homeless.title}"
