from django.db import models
from django.db.models import JSONField
from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

from .enums import LocationType, LanguageCode


class Location(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    center = models.PointField()
    parent_id = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    location_type = models.CharField(max_length=20, choices=LocationType.choices())#
    country_code = models.CharField(max_length=2)
    state_abbr = models.CharField(max_length=3)
    city = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def get_location_type_display(self):
        return LocationType[self.location_type].value
    

class Accommodation(models.Model):
    id = models.AutoField(primary_key=True)
    feed = models.PositiveSmallIntegerField(default=0)
    title = models.CharField(max_length=100)
    country_code = models.CharField(max_length=2)
    bedroom_count = models.PositiveIntegerField()
    review_score = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    usd_rate = models.DecimalField(max_digits=10, decimal_places=2)
    center = models.PointField()
    images = ArrayField(models.CharField(max_length=300), blank=True, default=list)
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE)
    amenities = ArrayField(models.CharField(max_length=100), blank=True, default=list)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    

class LocalizeAccommodation(models.Model):
    id = models.AutoField(primary_key=True)
    property_id = models.ForeignKey(Accommodation, on_delete=models.CASCADE)
    language = models.CharField(max_length=2, choices=LanguageCode.choices())#
    description = models.TextField()
    policy = JSONField(default=dict)

    def __str__(self):
        return f"Localized description for {self.property_id.title} ({self.language})"
