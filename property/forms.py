from django import forms
from .models import Property

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        # We exclude 'slug', 'created_at', and 'updated_at' because Django handles them automatically
        fields = [
            'title', 'description', 'property_type', 'status', 'price',
            'location', 'bedrooms', 'bathrooms', 'parking_spaces',
            'amenities', 'main_image', 'maps_iframe_url', 'is_featured'
        ]

    def __init__(self, *args, **kwargs):
        super(PropertyForm, self).__init__(*args, **kwargs)
        # Automatically add Tailwind classes to all form inputs for a mobile-first design
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'w-5 h-5 text-red-600 rounded border-gray-300 focus:ring-red-500'
            else:
                field.widget.attrs['class'] = 'w-full bg-gray-50 border border-gray-200 text-gray-900 px-4 py-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-600 transition shadow-inner'