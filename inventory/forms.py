from django import forms
from .models import Accommodation, AccommodationImage
from django.core.exceptions import ValidationError

class AccommodationForm(forms.ModelForm):
    # Field for uploading multiple images
    images_upload = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}),
        required=False
    )

    class Meta:
        model = Accommodation
        fields = [
            'title', 'country_code', 'bedroom_count', 'review_score',
            'usd_rate', 'center', 'location_id', 'amenities', 'published'
        ]
        widgets = {
            'center': forms.TextInput(attrs={'placeholder': 'Enter location point (e.g., POINT(lon lat))'}),
        }

    def clean_review_score(self):
        review_score = self.cleaned_data.get('review_score')
        if review_score < 0:
            raise ValidationError('Review score cannot be negative.')
        return review_score

    def clean_usd_rate(self):
        usd_rate = self.cleaned_data.get('usd_rate')
        if usd_rate < 0:
            raise ValidationError('USD rate cannot be negative.')
        return usd_rate

    def clean_center(self):
        center = self.cleaned_data.get('center')
        # Add validation for PointField if needed
        return center
