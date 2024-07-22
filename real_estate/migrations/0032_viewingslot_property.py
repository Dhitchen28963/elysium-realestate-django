# Generated by Django 5.0.6 on 2024-07-22 15:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('real_estate', '0031_alter_property_transaction_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='viewingslot',
            name='property',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='viewing_slots', to='real_estate.property'),
        ),
    ]
