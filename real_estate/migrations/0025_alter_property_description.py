# Generated by Django 4.2.13 on 2024-07-04 11:41

from django.db import migrations
import django_summernote.fields


class Migration(migrations.Migration):

    dependencies = [
        ('real_estate', '0024_alter_property_transaction_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='description',
            field=django_summernote.fields.SummernoteTextField(),
        ),
    ]