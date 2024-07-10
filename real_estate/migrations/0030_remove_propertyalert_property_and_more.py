# Generated by Django 5.0.6 on 2024-07-10 17:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('real_estate', '0029_remove_property_property_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='propertyalert',
            name='property',
        ),
        migrations.RemoveField(
            model_name='propertyalert',
            name='user',
        ),
        migrations.RemoveField(
            model_name='propertymessage',
            name='agent',
        ),
        migrations.RemoveField(
            model_name='propertymessage',
            name='property',
        ),
        migrations.RemoveField(
            model_name='propertymessage',
            name='user',
        ),
        migrations.RemoveField(
            model_name='savedsearch',
            name='user',
        ),
        migrations.DeleteModel(
            name='Message',
        ),
        migrations.DeleteModel(
            name='PropertyAlert',
        ),
        migrations.DeleteModel(
            name='PropertyMessage',
        ),
        migrations.DeleteModel(
            name='SavedSearch',
        ),
    ]
