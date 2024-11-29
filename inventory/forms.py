from django import forms
from .models import Accommodation

class AccommodationForm(forms.ModelForm):
    class Meta:
        model = Accommodation
        exclude = ('id', 'user_id', 'created_at', 'updated_at')
