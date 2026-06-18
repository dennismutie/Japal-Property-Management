from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

# Ensure we import both Property AND PropertyImage
from .models import Property, PropertyImage
from .forms import PropertyForm



# ==========================================
# PUBLIC VIEWS
# ==========================================

def home(request):
    # Fetch up to 21 featured properties, newest first
    # (21 is a great number because it's divisible by 3 for perfect grid rows)
    featured_properties = Property.objects.filter(is_featured=True).order_by('-created_at')[:21]
    return render(request, 'home.html', {'featured_properties': featured_properties})


def about(request):
    return render(request, 'about.html')


def services(request):
    return render(request, 'services.html')


def propertylisting(request):
    # 1. Fetch all properties by default
    properties = Property.objects.all()

    # 2. Capture search queries from the URL (e.g., ?location=Juja&type=apartment)
    location_query = request.GET.get('location')
    type_query = request.GET.get('type')
    status_query = request.GET.get('status')

    # 3. Filter the database based on the user's search
    if location_query:
        properties = properties.filter(location__icontains=location_query)

    if type_query:
        # .upper() ensures 'apartment' matches your model's 'APARTMENT'
        properties = properties.filter(property_type=type_query.upper())

    if status_query:
        properties = properties.filter(status=status_query.upper())

    # 4. Send the filtered properties to the template
    context = {
        'properties': properties,
        # Pass queries back to the template to keep the search bar populated
        'current_location': location_query,
    }
    return render(request, 'propertylisting.html', context)


def property_detail(request, pk):
    # Fetch the exact property using its Primary Key (pk/id)
    property_obj = get_object_or_404(Property, pk=pk)

    # Fetch all extra images associated with this property
    gallery_images = property_obj.gallery_images.all()

    context = {
        'property': property_obj,
        'gallery_images': gallery_images,  # Pass the gallery to the HTML template
    }
    return render(request, 'property_detail.html', context)


def contact(request):
    if request.method == 'POST':
        # Capture form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        inquiry_type = request.POST.get('inquiry_type')
        message = request.POST.get('message')

        # TODO: Add logic later to send an email to info@japalproperties.com

        # Flash a success message to the user
        messages.success(request, f"Thank you, {first_name}! Your message has been sent to JAPAL Property Management.")
        return redirect('contact')

    return render(request, 'contact.html')


# ==========================================
# CUSTOM ADMIN DASHBOARD VIEWS
# ==========================================

def custom_dashboard(request):
    """The main hub for the admin to see all posted properties."""
    # Fetch all properties, newest first
    properties = Property.objects.all().order_by('-created_at')

    context = {
        'properties': properties,
        'total_properties': properties.count(),
        'active_rentals': properties.filter(status='RENT').count(),
        'active_sales': properties.filter(status='SALE').count(),
    }
    return render(request, 'dashboard.html', context)


def add_property(request):
    """View to handle the posting of a new property WITH multiple gallery images."""
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            # Save main property but capture it in a variable
            new_property = form.save()

            # Catch multiple files from the HTML form named 'gallery_images'
            extra_images = request.FILES.getlist('gallery_images')
            for image in extra_images:
                PropertyImage.objects.create(property=new_property, image=image)

            messages.success(request, "Success! New property and gallery images have been published.")
            return redirect('custom_dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PropertyForm()

    return render(request, 'add_property.html', {'form': form})


def edit_property(request, pk):
    """View to edit an existing property and append new gallery images."""
    property_obj = get_object_or_404(Property, pk=pk)

    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=property_obj)
        if form.is_valid():
            # Save the updated main property
            updated_property = form.save()

            # Catch any newly uploaded extra files when editing
            extra_images = request.FILES.getlist('gallery_images')
            for image in extra_images:
                PropertyImage.objects.create(property=updated_property, image=image)

            messages.success(request, f"Success! '{property_obj.title}' was updated.")
            return redirect('custom_dashboard')
    else:
        form = PropertyForm(instance=property_obj)

    return render(request, 'add_property.html', {'form': form, 'is_edit': True, 'property': property_obj})


def delete_property(request, pk):
    """View to delete a property securely via POST request."""
    property_obj = get_object_or_404(Property, pk=pk)
    if request.method == 'POST':
        property_obj.delete()
        messages.success(request, "Listing successfully deleted.")
    return redirect('custom_dashboard')