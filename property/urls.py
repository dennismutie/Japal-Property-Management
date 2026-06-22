from django.urls import path
from . import views
from django.contrib.auth import views as auth_views  # Add this import!

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
# Admin Authentication URLs
    path('management-hub/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('management-hub/logout/', auth_views.LogoutView.as_view(), name='logout'),

path('insights/', views.blog_list, name='blog_list'),
    path('insights/<slug:slug>/', views.blog_detail, name='blog_detail'),

path('management-hub/blog/add/', views.add_blog, name='add_blog'),
    path('management-hub/blog/edit/<int:pk>/', views.edit_blog, name='edit_blog'),
    path('management-hub/blog/delete/<int:pk>/', views.delete_blog, name='delete_blog'),
]
