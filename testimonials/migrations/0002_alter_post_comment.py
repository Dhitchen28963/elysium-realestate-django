# Generated by Django 4.2.13 on 2024-07-04 11:41

from django.db import migrations
import django_summernote.fields


class Migration(migrations.Migration):

    dependencies = [
        ('testimonials', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='comment',
            field=django_summernote.fields.SummernoteTextField(),
        ),
    ]
