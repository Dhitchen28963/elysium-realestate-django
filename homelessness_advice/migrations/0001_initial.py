# Generated by Django 4.2.13 on 2024-05-27 09:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(unique=True)),
                ('featured_image', models.ImageField(default='default.jpg', upload_to='homelessness_advice_images/')),
                ('content', models.TextField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')], default='draft', max_length=10)),
                ('excerpt', models.TextField(blank=True, max_length=500)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='homelessness_advice_posts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
