# Generated by Django 4.2.13 on 2024-06-02 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('real_estate', '0015_alter_savedsearch_property_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='savedsearch',
            name='bathrooms_max',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='savedsearch',
            name='bathrooms_min',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
