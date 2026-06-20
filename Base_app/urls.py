"""
Base App URL Configuration
"""

from django.urls import path
from . import views

app_name = 'base'

urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('help/', views.help_page, name='help'),
    path('terms/', views.terms, name='terms'),
    path('privacy/', views.privacy, name='privacy'),
    path('safety/', views.safety, name='safety'),
    path('contact/', views.contact, name='contact'),
    path('categories/', views.browse_categories, name='categories'),
]