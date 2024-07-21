from django.db import models
from django.utils import timezone
from django_summernote.fields import SummernoteTextField
from cloudinary.models import CloudinaryField


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = SummernoteTextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    featured_image = CloudinaryField('image', default='placeholder')
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='posts'
    )

    def __str__(self):
        return self.title


class PropertyImage(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='additional_images'
    )
    image = CloudinaryField('image')

    def __str__(self):
        return f"Image for {self.post.title}"
