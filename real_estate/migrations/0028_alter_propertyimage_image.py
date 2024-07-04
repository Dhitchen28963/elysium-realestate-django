# Generated by Django 5.0.6 on 2024-07-04 18:31

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('real_estate', '0027_rename_featured_image_property_property_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='propertyimage',
            name='image',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='image'),
        ),
    ]
