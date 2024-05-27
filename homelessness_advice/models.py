from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='homelessness_advice_posts')
    featured_image = models.ImageField(upload_to='homelessness_advice_images/', default='default.jpg')
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    excerpt = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.title
