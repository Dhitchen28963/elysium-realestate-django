# Generated by Django 4.2.13 on 2024-06-02 17:22

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('student_accommodation', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='studentproperty',
            old_name='status',
            new_name='availability_status',
        ),
        migrations.AddField(
            model_name='studentproperty',
            name='publication_status',
            field=models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')], default='draft', max_length=10),
        ),
        migrations.CreateModel(
            name='ViewingSlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('is_booked', models.BooleanField(default=False)),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_agent_slots', to=settings.AUTH_USER_MODEL)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='viewing_slots', to='student_accommodation.studentproperty')),
            ],
        ),
        migrations.CreateModel(
            name='ViewingAppointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Anonymous', max_length=255)),
                ('contact', models.CharField(default='Unknown', max_length=255)),
                ('email', models.EmailField(default='example@example.com', max_length=254)),
                ('message', models.TextField(default='No message')),
                ('preferred_date', models.DateField(default=datetime.date.today)),
                ('preferred_time', models.TimeField(default=datetime.time(9, 0))),
                ('is_scheduled', models.BooleanField(default=False)),
                ('attended', models.BooleanField(default=False)),
                ('viewing_decision', models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending', max_length=10)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('agent_name', models.CharField(blank=True, max_length=255, null=True)),
                ('agent_contact', models.CharField(blank=True, max_length=255, null=True)),
                ('agent_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='student_accommodation.studentproperty')),
                ('slot', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='appointments', to='student_accommodation.viewingslot')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_viewing_appointments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StudentPropertyMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('message', models.TextField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('agent', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='student_agent_messages', to=settings.AUTH_USER_MODEL)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='student_accommodation.studentproperty')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_property_messages', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SavedSearch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('search_name', models.CharField(max_length=255)),
                ('location', models.CharField(blank=True, max_length=100, null=True)),
                ('property_type', models.CharField(blank=True, choices=[('detached-houses', 'Detached houses'), ('semi-detached-houses', 'Semi-detached houses'), ('terraced-houses', 'Terraced houses'), ('mobile-park-homes', 'Mobile / Park homes'), ('boats', 'Boats'), ('flats-apartments', 'Flats / Apartments'), ('bungalows', 'Bungalows'), ('land', 'Land'), ('commercial-property', 'Commercial Property'), ('hmo', "HMO's")], max_length=20, null=True)),
                ('bedrooms_min', models.PositiveIntegerField(blank=True, null=True)),
                ('bedrooms_max', models.PositiveIntegerField(blank=True, null=True)),
                ('bathrooms_min', models.PositiveIntegerField(blank=True, null=True)),
                ('bathrooms_max', models.PositiveIntegerField(blank=True, null=True)),
                ('price_min', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('price_max', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('garden', models.BooleanField(default=False)),
                ('parking', models.BooleanField(default=False)),
                ('pets_allowed', models.BooleanField(default=False)),
                ('furnished_type', models.CharField(blank=True, choices=[('furnished', 'Furnished'), ('unfurnished', 'Unfurnished'), ('part_furnished', 'Part Furnished')], max_length=20, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_saved_searches', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PropertyAlert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('seen', models.BooleanField(default=False)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='alerts', to='student_accommodation.studentproperty')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_property_alerts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FavoriteProperty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='student_accommodation.studentproperty')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_favorite_properties', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'property')},
            },
        ),
    ]
