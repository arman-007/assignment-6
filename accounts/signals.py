# accounts/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

@receiver(post_save, sender=User)
def assign_property_owner_group(sender, instance, created, **kwargs):
    if not created:
        # Check if the user is activated and not already in the group
        if instance.is_active and not instance.groups.filter(name="Property owner").exists():
            try:
                property_owner_group = Group.objects.get(name="Property owner")
            except Group.DoesNotExist:
                # Optionally, create the group if it doesn't exist
                property_owner_group = Group.objects.create(name="Property owner")
                # Assign relevant permissions to the group
                # Example: Add permissions to manage Accommodation
                from django.contrib.contenttypes.models import ContentType
                from django.contrib.auth.models import Permission
                from inventory.models import Accommodation  # Adjust app name as necessary
                
                accommodation_ct = ContentType.objects.get_for_model(Accommodation)
                permissions = Permission.objects.filter(content_type=accommodation_ct)
                property_owner_group.permissions.set(permissions)
            instance.groups.add(property_owner_group)
