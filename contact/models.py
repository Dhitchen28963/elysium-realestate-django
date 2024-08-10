from django.db import models

"""
Defines the ContactMessage model to store contact messages from users.
Each message includes the sender's name, email, message content, and the
timestamp of when it was created.
"""


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} ({self.email})"
