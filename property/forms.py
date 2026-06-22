from django import forms
from .models import Property
# Make sure BlogPost is added to this import list!
from .models import Property, PropertyImage, BlogPost

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


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'thumbnail', 'summary', 'content', 'is_published']

        # Adding some basic Tailwind classes so it looks good in the admin dashboard
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-lg focus:bg-white focus:ring-2 focus:ring-red-600 outline-none'}),
            'summary': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-lg focus:bg-white focus:ring-2 focus:ring-red-600 outline-none resize-none',
                'rows': 2}),
            'content': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-lg focus:bg-white focus:ring-2 focus:ring-red-600 outline-none',
                'rows': 10}),
            'is_published': forms.CheckboxInput(
                attrs={'class': 'w-5 h-5 text-red-600 border-gray-300 rounded focus:ring-red-600'}),
        }