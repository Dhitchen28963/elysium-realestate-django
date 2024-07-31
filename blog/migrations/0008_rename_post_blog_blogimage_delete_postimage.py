# Generated by Django 5.0.6 on 2024-07-28 22:10

import cloudinary.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_alter_post_content'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Post',
            new_name='Blog',
        ),
        migrations.CreateModel(
            name='BlogImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', cloudinary.models.CloudinaryField(max_length=255, verbose_name='image')),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='additional_images', to='blog.blog')),
            ],
        ),
        migrations.DeleteModel(
            name='PostImage',
        ),
    ]