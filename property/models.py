from django.db import models
from django.utils.text import slugify


class Property(models.Model):
    STATUS_CHOICES = [
        ('RENT', 'To Let'),
        ('SALE', 'For Sale'),
    ]

    TYPE_CHOICES = [
        ('APARTMENT', 'Apartment'),
        ('COMMERCIAL', 'Commercial Space'),
        ('LAND', 'Land / Plot'),
        ('TOWNHOUSE', 'Townhouse'),
    ]

    # Fixed all instances of max_w to max_length
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, max_length=250)
    description = models.TextField()
    property_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='APARTMENT')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='RENT')
    price = models.DecimalField(max_digits=12, decimal_places=2)
    location = models.CharField(max_length=100, help_text="e.g. Juja, Westlands, Milimani")

    # Amenities / Specs
    bedrooms = models.IntegerField(default=0, verbose_name="Bedrooms (0 for Land)")
    bathrooms = models.IntegerField(default=0, verbose_name="Bathrooms")
    parking_spaces = models.IntegerField(default=0, verbose_name="Parking Spaces")
    amenities = models.TextField(blank=True, help_text="Comma-separated list, e.g. Borehole, Backup Generator, Gym")

    # Media & Map
    main_image = models.ImageField(upload_to='properties/thumbnails/')
    maps_iframe_url = models.TextField(blank=True,
                                       help_text="Paste the src link inside the Google Maps embed code iframe")

    # Admin Controls
    is_featured = models.BooleanField(default=False, help_text="Pin this property to the homepage featured grid")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Properties"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class PropertyImage(models.Model):
    """Allows an individual property to have an infinite gallery of images."""
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ImageField(upload_to='properties/gallery/')

    def __str__(self):
        return f"Gallery Image for {self.property.title}"