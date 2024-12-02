from django.contrib import admin
from .models import Location, Accommodation, LocalizeAccommodation
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'email', 'is_active', 'date_joined']
    list_filter = ['is_active', 'is_staff']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'is_active', 'is_staff', 'groups')}
        ),
    )

# Register the custom UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


# Custom Admin for Location model
class LocationAdmin(admin.ModelAdmin):
    list_display = ('title', 'city', 'location_type', 'country_code')
    list_filter = ('location_type', 'country_code', 'city')  # Add filters for location_type, country_code, and city
    search_fields = ('title', 'city', 'country_code')  # Allow searching by title, city, or country_code

admin.site.register(Location, LocationAdmin)


# Custom Admin for Accommodation model
class AccommodationAdmin(admin.ModelAdmin):
    list_display = ['title', 'country_code', 'bedroom_count', 'review_score', 'usd_rate', 'location_id']
    
    def get_queryset(self, request):
        """
        Limit the queryset so that a property owner can only see their own properties.
        """
        queryset = super().get_queryset(request)
        
        if request.user.is_superuser:
            return queryset  # Superusers can see all properties
        
        # Property owners can only see their own properties
        if request.user.groups.filter(name="Property owner").exists():
            return queryset.filter(owner=request.user)  # assuming you have a foreign key to the user in Accommodation model

        return queryset

admin.site.register(Accommodation, AccommodationAdmin)


# Custom Admin for LocalizeAccommodation model
class LocalizeAccommodationAdmin(admin.ModelAdmin):
    list_display = ('policy', 'language', 'description')
    list_filter = [('language')]  # Filter by language and created_at date
    search_fields = ('description',)  # Allow searching by description

admin.site.register(LocalizeAccommodation, LocalizeAccommodationAdmin)

