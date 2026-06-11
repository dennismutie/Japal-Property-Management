from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Property
from .forms import PropertyForm  # Import our new form

from django.shortcuts import get_object_or_404


def home(request):
    # Fetch up to 3 featured properties, newest first
    featured_properties = Property.objects.filter(is_featured=True).order_by('-created_at')[:3]
    return render(request, 'home.html', {'featured_properties': featured_properties})


def about(request):
    return render(request, 'about.html')


def services(request):
    return render(request, 'services.html')


def propertylisting(request):
    # This will render the propertylisting.html template when we build it
    return render(request, 'propertylisting.html')


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



from .models import Property  # Import your new model





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


def contact(request):
    # ... (Keep your existing contact view logic here) ...
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
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
    """View to handle the posting of a new property."""
    if request.method == 'POST':
        # request.FILES is crucial for capturing the uploaded image!
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Success! New property has been published.")
            return redirect('custom_dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PropertyForm()

    return render(request, 'add_property.html', {'form': form})




def edit_property(request, pk):
    """View to edit an existing property."""
    property_obj = get_object_or_404(Property, pk=pk)

    if request.method == 'POST':
        # instance=property_obj tells Django to update, not create new
        form = PropertyForm(request.POST, request.FILES, instance=property_obj)
        if form.is_valid():
            form.save()
            messages.success(request, f"Success! '{property_obj.title}' was updated.")
            return redirect('custom_dashboard')
    else:
        form = PropertyForm(instance=property_obj)

    return render(request, 'add_property.html', {'form': form, 'is_edit': True})


def delete_property(request, pk):
    """View to delete a property securely via POST request."""
    property_obj = get_object_or_404(Property, pk=pk)
    if request.method == 'POST':
        property_obj.delete()
        messages.success(request, "Listing successfully deleted.")
    return redirect('custom_dashboard')