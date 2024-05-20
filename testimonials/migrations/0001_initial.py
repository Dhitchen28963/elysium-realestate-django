# Generated by Django 4.2.13 on 2024-05-20 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Testimonial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('testimonial', models.TextField()),
                ('rating', models.PositiveIntegerField()),
            ],
        ),
    ]