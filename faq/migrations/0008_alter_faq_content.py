# Generated by Django 5.0.6 on 2024-07-28 23:12

import django_summernote.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('faq', '0007_alter_faq_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faq',
            name='content',
            field=django_summernote.fields.SummernoteTextField(),
        ),
    ]
