from django.core.management.base import BaseCommand
from property_guides.models import Post, Category

class Command(BaseCommand):
    help = 'Update post categories to use Category model'

    def handle(self, *args, **kwargs):
        for post in Post.objects.all():
            if isinstance(post.category, str):
                try:
                    category, created = Category.objects.get_or_create(name=post.category)
                    post.category = category
                    post.save()
                    self.stdout.write(self.style.SUCCESS(f'Successfully updated category for post {post.title}'))
                except Category.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f'Category "{post.category}" does not exist'))
