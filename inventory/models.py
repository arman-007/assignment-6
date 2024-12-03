from django.db import models
from django.db.models import JSONField
from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

from .enums import LocationType, LanguageCode


class Location(models.Model):
    # ID field (Primary Key)
    id = models.AutoField(primary_key=True)
    # Title field (name of the location)
    title = models.CharField(max_length=100)
    # Geolocation (PostGIS point)
    center = models.PointField()
    # Parent Location (ForeignKey to itself for hierarchical structure)
    parent_id = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    # Location type (continent, country, state, city, etc.)
    location_type = models.CharField(max_length=20, choices=LocationType.choices())#
    # ISO country code (2 characters)
    country_code = models.CharField(max_length=2)
    # State abbreviation (3 characters)
    state_abbr = models.CharField(max_length=3)
    # City name
    city = models.CharField(max_length=30)
    # Created timestamp (auto-generated on creation)
    created_at = models.DateTimeField(auto_now_add=True)
    # Updated timestamp (auto-updated on every save)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def get_location_type_display(self):
        return LocationType[self.location_type].value
    

class Accommodation(models.Model):
    # ID field (Primary Key)
    id = models.AutoField(primary_key=True)
    # Feed number (small unsigned integer, default 0)
    feed = models.PositiveSmallIntegerField(default=0)
    # Title (name of the accommodation)
    title = models.CharField(max_length=100)
    # ISO country code (2 characters)
    country_code = models.CharField(max_length=2)
    # Bedroom count (unsigned integer)
    bedroom_count = models.PositiveIntegerField()
    # Review score (numeric with 1 decimal place, default 0)
    review_score = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    # USD rate (price rate in USD, with 2 decimal places)
    usd_rate = models.DecimalField(max_digits=10, decimal_places=2)
    # Geolocation (PostGIS point)
    center = models.PointField()
    # Location (Foreign Key to Location model)
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE)
    # Amenities (Array of JSONB objects with each amenity max 100 characters)
    amenities = ArrayField(models.CharField(max_length=100), blank=True, default=list)
    # User (Foreign Key to Django's User model, set automatically on creation)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    # Published (Boolean, default is False)
    published = models.BooleanField(default=False)
    # Created timestamp (auto-generated on creation)
    created_at = models.DateTimeField(auto_now_add=True)
    # Updated timestamp (auto-updated on every save)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    

class AccommodationImage(models.Model):
    accommodation = models.ForeignKey(Accommodation, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='accommodation_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.accommodation.title}"
    

class LocalizeAccommodation(models.Model):
    # ID field (auto-incremented)
    id = models.AutoField(primary_key=True)
    # Foreign Key to Accommodation model
    property_id = models.ForeignKey(Accommodation, on_delete=models.CASCADE)
    # Language code (2 characters)
    language = models.CharField(max_length=2, choices=LanguageCode.choices())#
    # Localized description (text)
    description = models.TextField()
    # Policy (JSONB dictionary, for example {"pet_policy": "value"})
    policy = JSONField(default=dict)

    def __str__(self):
        return f"Localized description for {self.property_id.title} ({self.language})"
