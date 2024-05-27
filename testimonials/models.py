from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=255)
    comment = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='testimonial_posts')

    def __str__(self):
        return self.title
