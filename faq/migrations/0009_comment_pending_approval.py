# Generated by Django 5.0.6 on 2024-08-06 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faq', '0008_alter_faq_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='pending_approval',
            field=models.BooleanField(default=False),
        ),
    ]
