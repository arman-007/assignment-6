# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from .models import Accommodation, AccommodationImage
# from .forms import AccommodationForm
# from django.conf import settings
# import os

# # List properties (accessible by the property owner)
# @login_required
# def property_list(request):
#     properties = Accommodation.objects.filter(owner=request.user)  # Assuming user has a foreign key to accommodation
#     return render(request, 'inventory/property_list.html', {'properties': properties})

# # Create a new property
# @login_required
# def property_create(request):
#     if request.method == 'POST':
#         form = AccommodationForm(request.POST, request.FILES)
#         if form.is_valid():
#             # Save the accommodation object
#             accommodation = form.save()

#             # Handle image uploads
#             images = request.FILES.getlist('images_upload')  # Get list of uploaded images
#             for image in images:
#                 # Save each image as a new AccommodationImage object
#                 AccommodationImage.objects.create(
#                     accommodation=accommodation,
#                     image=image
#                 )

#             return redirect('accommodation_detail', pk=accommodation.pk)
#     else:
#         form = AccommodationForm()

#     return render(request, 'inventory/accommodation_form.html', {'form': form})

# # Edit an existing property
# @login_required
# def property_edit(request, property_id):
#     property = Accommodation.objects.get(id=property_id)
#     if request.method == 'POST':
#         # handle form submission to update property
#         pass
#     return render(request, 'inventory/property_edit.html', {'property': property})

# # Delete a property
# @login_required
# def property_delete(request, property_id):
#     property = Accommodation.objects.get(id=property_id)
#     property.delete()
#     return redirect('property_list')
