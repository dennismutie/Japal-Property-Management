from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('properties/', views.propertylisting, name='propertylisting'),
    path('contact/', views.contact, name='contact'),

# Custom Dashboard URLs
    path('management-hub/', views.custom_dashboard, name='custom_dashboard'),
    path('management-hub/add/', views.add_property, name='add_property'),
    path('management-hub/edit/<int:pk>/', views.edit_property, name='edit_property'),
    path('management-hub/delete/<int:pk>/', views.delete_property, name='delete_property'),

# ADD THIS EXACT LINE HERE:
    path('properties/<int:pk>/', views.property_detail, name='property_detail'),
]