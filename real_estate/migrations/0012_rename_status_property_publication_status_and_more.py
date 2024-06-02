# Generated by Django 4.2.13 on 2024-06-01 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('real_estate', '0011_viewingappointment_viewing_decision'),
    ]

    operations = [
        migrations.RenameField(
            model_name='property',
            old_name='status',
            new_name='publication_status',
        ),
        migrations.AddField(
            model_name='property',
            name='availability_status',
            field=models.CharField(choices=[('available', 'Available'), ('unavailable', 'Unavailable')], default='available', max_length=15),
        ),
    ]