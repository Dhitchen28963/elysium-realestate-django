from django.db import models
from django.contrib.auth.models import User

class Testimonial(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='testimonials')
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Testimonial by {self.author}'
