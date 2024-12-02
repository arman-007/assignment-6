from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

@receiver(post_save, sender=get_user_model())
def assign_property_owner_group(sender, instance, created, **kwargs):
    if not created:
        return  # Don't run on creation
    if instance.is_active:
        property_owner_group = Group.objects.get(name="Property owner")
        instance.groups.add(property_owner_group)
        instance.save()
