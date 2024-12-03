# # inventory/forms.py
# from django import forms
# from .models import Accommodation
# from django.utils.crypto import get_random_string
# from django.core.files.storage import default_storage
# import os

# class AccommodationAdminForm(forms.ModelForm):
#     # Field for uploading multiple images
#     image_upload = forms.FileField(
#         widget=forms.ClearableFileInput(attrs={'multiple': True}),
#         required=False,
#         label='Upload Images'
#     )

#     class Meta:
#         model = Accommodation
#         exclude = ('user',)  # Exclude 'user' field from the form

#     def clean_image_upload(self):
#         images = self.files.getlist('image_upload')
#         for image in images:
#             if not image.content_type.startswith('image/'):
#                 raise forms.ValidationError(f"File {image.name} is not an image.")
#         return images

#     def save(self, commit=True, user=None):
#         accommodation = super().save(commit=False)
#         if user and not accommodation.user:
#             accommodation.user = user  # Assign the logged-in user

#         if commit:
#             accommodation.save()

#             # Handle image uploads
#             images = self.cleaned_data.get('image_upload')
#             if images:
#                 existing_images = accommodation.images if accommodation.images else []
#                 for image in images:
#                     # Generate a unique filename
#                     filename = get_random_string(length=32) + os.path.splitext(image.name)[1]
#                     # Define the path where the image will be saved
#                     path = os.path.join('accommodation_images', filename)
#                     # Save the image to MEDIA_ROOT/accommodation_images/
#                     saved_path = default_storage.save(path, image)
#                     # Get the URL
#                     image_url = default_storage.url(saved_path)
#                     # Append to the images list
#                     existing_images.append(image_url)

#                 # Update the images ArrayField
#                 accommodation.images = existing_images
#                 accommodation.save()

#         return accommodation
