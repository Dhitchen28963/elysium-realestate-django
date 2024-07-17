# Generated by Django 5.0.6 on 2024-07-04 18:15

import cloudinary.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faq', '0003_alter_faq_featured_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='FAQImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', cloudinary.models.CloudinaryField(max_length=255, verbose_name='image')),
                ('faq', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='additional_images', to='faq.faq')),
            ],
        ),
    ]