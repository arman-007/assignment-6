# from django.shortcuts import render
# from allauth.account.views import LoginView


# class CustomLoginView(LoginView):
#     template_name = 'account/login.html'

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Accommodation

@login_required
def user_properties(request):
    # Only show properties owned by the logged-in user
    properties = Accommodation.objects.filter(user=request.user)
    return render(request, 'user_properties.html', {'properties': properties})
