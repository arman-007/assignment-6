from django.contrib import admin
from .models import Location, Accommodation, LocalizeAccommodation

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['title', 'city', 'location_type', 'country_code']

@admin.register(Accommodation)
class AccommodationAdmin(admin.ModelAdmin):
    list_display = ['title', 'country_code', 'usd_rate', 'bedroom_count', 'published']
    search_fields = ['title', 'country_code']

@admin.register(LocalizeAccommodation)
class LocalizeAccommodationAdmin(admin.ModelAdmin):
    list_display = ['policy', 'language', 'description']
