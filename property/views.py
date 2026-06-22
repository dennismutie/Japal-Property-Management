from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Consolidated imports
from .models import Property, PropertyImage, BlogPost
from .forms import PropertyForm, BlogPostForm  # Make sure to create BlogPostForm in forms.py

from .models import Property, BlogPost  # Ensure both models are imported

# ==========================================
# PUBLIC VIEWS
# ==========================================

def home(request):
    # Fetch up to 21 featured properties
    featured_properties = Property.objects.filter(is_featured=True).order_by('-created_at')[:21]

    # Fetch the 3 most recent published blog posts
    latest_posts = BlogPost.objects.filter(is_published=True).order_by('-created_at')[:3]

    # Bundle both into the context dictionary
    context = {
        'featured_properties': featured_properties,
        'latest_posts': latest_posts,
    }

    return render(request, 'home.html', context)
def about(request):
    return render(request, 'about.html')


def services(request):
    return render(request, 'services.html')


def propertylisting(request):
    properties = Property.objects.all()

    location_query = request.GET.get('location')
    type_query = request.GET.get('type')
    status_query = request.GET.get('status')
    sort_query = request.GET.get('sort')

    if location_query:
        properties = properties.filter(location__icontains=location_query)

    if type_query:
        properties = properties.filter(property_type=type_query.upper())

    if status_query:
        properties = properties.filter(status=status_query.upper())

    if sort_query == 'price_low':
        properties = properties.order_by('price')
    elif sort_query == 'price_high':
        properties = properties.order_by('-price')
    else:
        properties = properties.order_by('-created_at')

    context = {
        'properties': properties,
        'current_location': location_query,
        'current_type': type_query,
        'current_status': status_query,
        'current_sort': sort_query,
    }
    return render(request, 'propertylisting.html', context)


def property_detail(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    gallery_images = property_obj.gallery_images.all()

    context = {
        'property': property_obj,
        'gallery_images': gallery_images,
    }
    return render(request, 'property_detail.html', context)


def contact(request):
    """Renders the contact page. Form data is offloaded directly to WhatsApp via JavaScript."""
    return render(request, 'contact.html')


def blog_list(request):
    """Fetches all published blog posts, newest first."""
    posts = BlogPost.objects.filter(is_published=True).order_by('-created_at')
    return render(request, 'blog_list.html', {'posts': posts})


def blog_detail(request, slug):
    """Fetches a specific blog post using its unique slug."""
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    recent_posts = BlogPost.objects.filter(is_published=True).exclude(id=post.id).order_by('-created_at')[:3]
    return render(request, 'blog_detail.html', {'post': post, 'recent_posts': recent_posts})


# ==========================================
# CUSTOM ADMIN DASHBOARD VIEWS
# ==========================================

@login_required
def custom_dashboard(request):
    """The main hub for the admin to see all posted properties and blogs."""
    properties = Property.objects.all().order_by('-created_at')
    posts = BlogPost.objects.all().order_by('-created_at')

    context = {
        'properties': properties,
        'total_properties': properties.count(),
        'active_rentals': properties.filter(status='RENT').count(),
        'active_sales': properties.filter(status='SALE').count(),

        'posts': posts,
        'total_posts': posts.count(),
    }
    return render(request, 'dashboard.html', context)


# --- PROPERTY ADMIN VIEWS ---

@login_required
def add_property(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            new_property = form.save()
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


@login_required
def edit_property(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)

    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=property_obj)
        if form.is_valid():
            updated_property = form.save()
            extra_images = request.FILES.getlist('gallery_images')
            for image in extra_images:
                PropertyImage.objects.create(property=updated_property, image=image)
            messages.success(request, f"Success! '{property_obj.title}' was updated.")
            return redirect('custom_dashboard')
    else:
        form = PropertyForm(instance=property_obj)

    return render(request, 'add_property.html', {'form': form, 'is_edit': True, 'property': property_obj})


@login_required
def delete_property(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    if request.method == 'POST':
        property_obj.delete()
        messages.success(request, "Listing successfully deleted.")
    return redirect('custom_dashboard')


# --- BLOG ADMIN VIEWS ---

@login_required
def add_blog(request):
    """View to handle the posting of a new blog article."""
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            new_blog = form.save(commit=False)
            new_blog.author = request.user  # Automatically assign logged-in user as author
            new_blog.save()
            messages.success(request, "Success! New blog post has been saved.")
            return redirect('custom_dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = BlogPostForm()

    return render(request, 'add_blog.html', {'form': form})


@login_required
def edit_blog(request, pk):
    """View to edit an existing blog article."""
    post_obj = get_object_or_404(BlogPost, pk=pk)

    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post_obj)
        if form.is_valid():
            form.save()
            messages.success(request, f"Success! '{post_obj.title}' was updated.")
            return redirect('custom_dashboard')
    else:
        form = BlogPostForm(instance=post_obj)

    return render(request, 'add_blog.html', {'form': form, 'is_edit': True, 'post': post_obj})


@login_required
def delete_blog(request, pk):
    """View to delete a blog article securely via POST request."""
    post_obj = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        post_obj.delete()
        messages.success(request, "Blog post successfully deleted.")
    return redirect('custom_dashboard')