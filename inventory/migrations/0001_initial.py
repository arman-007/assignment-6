# Generated by Django 5.1.3 on 2024-12-04 18:57

import django.contrib.gis.db.models.fields
import django.contrib.postgres.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Accommodation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('feed', models.PositiveSmallIntegerField(default=0)),
                ('title', models.CharField(max_length=100)),
                ('country_code', models.CharField(max_length=2)),
                ('bedroom_count', models.PositiveIntegerField()),
                ('review_score', models.DecimalField(decimal_places=1, default=0, max_digits=2)),
                ('usd_rate', models.DecimalField(decimal_places=2, max_digits=10)),
                ('center', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('images', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=300), blank=True, default=list, size=None)),
                ('amenities', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), blank=True, default=list, size=None)),
                ('published', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LocalizeAccommodation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('language', models.CharField(choices=[('en', 'ENGLISH'), ('fr', 'FRENCH'), ('es', 'SPANISH'), ('de', 'GERMAN'), ('it', 'ITALIAN'), ('pt', 'PORTUGUESE'), ('zh', 'CHINESE'), ('ar', 'ARABIC'), ('ja', 'JAPANESE'), ('ru', 'RUSSIAN'), ('bn', 'BENGALI'), ('hi', 'HINDI'), ('ur', 'URDU'), ('ko', 'KOREAN'), ('tr', 'TURKISH'), ('pl', 'POLISH'), ('nl', 'DUTCH'), ('sv', 'SWEDISH'), ('el', 'GREEK'), ('ro', 'ROMANIAN'), ('da', 'DANISH'), ('fi', 'FINNISH'), ('cs', 'CZECH'), ('hu', 'HUNGARIAN'), ('bg', 'BULGARIAN'), ('sk', 'SLOVAK'), ('sl', 'SLOVENIAN'), ('hr', 'CROATIAN'), ('sr', 'SERBIAN'), ('bs', 'BOSNIAN'), ('mk', 'MACEDONIAN'), ('lv', 'LATVIAN'), ('lt', 'LITHUANIAN'), ('et', 'ESTONIAN'), ('uk', 'UKRAINIAN'), ('be', 'BELARUSIAN'), ('ka', 'GEORGIAN'), ('hy', 'ARMENIAN'), ('fa', 'PERSIAN'), ('th', 'THAI'), ('vi', 'VIETNAMESE'), ('ms', 'MALAY'), ('id', 'INDONESIAN'), ('tl', 'TAGALOG'), ('sw', 'SWAHILI'), ('zu', 'ZULU'), ('am', 'AMHARIC'), ('so', 'SOMALI'), ('ta', 'TAMIL'), ('te', 'TELUGU'), ('kn', 'KANNADA'), ('ml', 'MALAYALAM'), ('si', 'SINHALESE'), ('my', 'BURMESE'), ('lo', 'LAO'), ('km', 'KHMERS'), ('bo', 'TIBETAN'), ('ne', 'NEPALI'), ('is', 'ICELANDIC'), ('no', 'NORWEGIAN'), ('he', 'HEBREW'), ('yi', 'YIDDISH')], max_length=2)),
                ('description', models.TextField()),
                ('policy', models.JSONField(default=dict)),
                ('property_id', models.ForeignKey(db_column='property_id', on_delete=django.db.models.deletion.CASCADE, to='inventory.accommodation')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('center', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('location_type', models.CharField(choices=[('COUNTRY', 'COUNTRY'), ('STATE', 'STATE'), ('CITY', 'CITY')], max_length=20)),
                ('country_code', models.CharField(max_length=2)),
                ('state_abbr', models.CharField(max_length=3)),
                ('city', models.CharField(max_length=30)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('parent_id', models.ForeignKey(blank=True, db_column='parent_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='inventory.location')),
            ],
        ),
        migrations.AddField(
            model_name='accommodation',
            name='location_id',
            field=models.ForeignKey(db_column='location_id', on_delete=django.db.models.deletion.CASCADE, to='inventory.location'),
        ),
    ]
