from django.db import models

class HomelessSupport(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    contact_info = models.TextField()

    def __str__(self):
        return self.title