from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django.contrib.auth.models import User

class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        # Deactivate user upon registration and make them a staff member
        user.is_active = False  # Deactivate user by default
        user.is_staff = True  # Make them staff
        user.save()
        return user
