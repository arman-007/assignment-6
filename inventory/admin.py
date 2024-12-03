from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html

from .models import Location, Accommodation, LocalizeAccommodation, AccommodationImage


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
    list_filter = ('location_type', 'country_code')  # Add filters for location_type, country_code, and city
    search_fields = ('title', 'city', 'country_code')  # Allow searching by title, city, or country_code

admin.site.register(Location, LocationAdmin)


class AccommodationImageInline(admin.TabularInline):
    model = AccommodationImage
    extra = 1  # Number of extra forms to display
    readonly_fields = ('image_preview',)
    fields = ('image', 'image_preview')  # Fields to display in the inline

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px;"/>', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Image Preview'

class AccommodationAdmin(admin.ModelAdmin):
    list_display = ['title', 'country_code', 'bedroom_count', 'review_score', 'usd_rate', 'published']
    list_filter = ['published', 'country_code']
    search_fields = ['title', 'country_code']
    exclude = ('user',)  # Exclude the 'user' field from the admin form
    inlines = [AccommodationImageInline]  # Add the inline images

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif request.user.groups.filter(name='Property owner').exists():
            return qs.filter(user=request.user)
        return qs.none()

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user  # Automatically assign the logged-in user as the owner
        obj.save()

admin.site.register(Accommodation, AccommodationAdmin)


# Custom Admin for LocalizeAccommodation model
class LocalizeAccommodationAdmin(admin.ModelAdmin):
    list_display = ('policy', 'language', 'description')
    list_filter = [('language')]  # Filter by language and created_at date
    search_fields = ('description',)  # Allow searching by description

admin.site.register(LocalizeAccommodation, LocalizeAccommodationAdmin)

