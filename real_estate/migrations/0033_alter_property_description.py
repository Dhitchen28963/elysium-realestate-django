# Generated by Django 5.0.6 on 2024-07-28 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('real_estate', '0032_viewingslot_property'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='description',
            field=models.TextField(),
        ),
    ]