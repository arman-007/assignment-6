# Generated by Django 5.1.3 on 2024-12-04 04:13

import inventory.enums
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_alter_location_location_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='location_type',
            field=models.CharField(choices=[(inventory.enums.LocationType['COUNTRY'], 'COUNTRY'), (inventory.enums.LocationType['STATE'], 'STATE'), (inventory.enums.LocationType['CITY'], 'CITY')], max_length=20),
        ),
    ]
