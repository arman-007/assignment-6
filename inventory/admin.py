from django.contrib import admin
from .models import Location, Accommodation, LocalizeAccommodation


# Custom Admin for Location model
class LocationAdmin(admin.ModelAdmin):
    list_display = ('title', 'city', 'location_type', 'country_code')
    list_filter = ('location_type', 'country_code', 'city')  # Add filters for location_type, country_code, and city
    search_fields = ('title', 'city', 'country_code')  # Allow searching by title, city, or country_code

admin.site.register(Location, LocationAdmin)


# Custom Admin for Accommodation model
class AccommodationAdmin(admin.ModelAdmin):
    list_display = ('title', 'country_code', 'usd_rate', 'bedroom_count', 'published')
    list_filter = ('country_code', 'bedroom_count', 'review_score', 'published')  # Filter by country, bedroom count, review score, and published status
    search_fields = ('title', 'country_code')  # Allow searching by title or country_code

admin.site.register(Accommodation, AccommodationAdmin)


# Custom Admin for LocalizeAccommodation model
class LocalizeAccommodationAdmin(admin.ModelAdmin):
    list_display = ('policy', 'language', 'description')
    list_filter = [('language')]  # Filter by language and created_at date
    search_fields = ('description',)  # Allow searching by description

admin.site.register(LocalizeAccommodation, LocalizeAccommodationAdmin)

