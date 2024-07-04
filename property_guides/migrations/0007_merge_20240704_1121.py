from django.db import migrations

def create_initial_categories(apps, schema_editor):
    Category = apps.get_model('property_guides', 'Category')
    initial_categories = [
        'Landlord',
        'Renter',
        'Student',
        'Neighbour Disputes',
        'Repairs',
        'Fire Safety',
        'Complaints',
        'Eviction',
    ]
    for category_name in initial_categories:
        Category.objects.create(name=category_name)

class Migration(migrations.Migration):

    dependencies = [
        ('property_guides', '0005_category_alter_post_category'),
        ('property_guides', '0006_auto_20240704_1119'),
    ]

    operations = [
        migrations.RunPython(create_initial_categories),
    ]