# Generated by Django 4.2.13 on 2024-06-02 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('real_estate', '0014_savedsearch_propertyalert'),
    ]

    operations = [
        migrations.AlterField(
            model_name='savedsearch',
            name='property_type',
            field=models.CharField(blank=True, choices=[('detached-houses', 'Detached houses'), ('semi-detached-houses', 'Semi-detached houses'), ('terraced-houses', 'Terraced houses'), ('mobile-park-homes', 'Mobile / Park homes'), ('boats', 'Boats'), ('flats-apartments', 'Flats / Apartments'), ('bungalows', 'Bungalows'), ('land', 'Land'), ('commercial-property', 'Commercial Property'), ('hmo', "HMO's")], max_length=20, null=True),
        ),
    ]
