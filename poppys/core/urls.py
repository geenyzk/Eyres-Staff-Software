"""core/urls.py
Add a root route so hitting "/" does not 404. We redirect to the
named "login" route in the accounts app.
"""
from django.urls import path
from django.views.generic.base import RedirectView
from .views import landing_view

urlpatterns = [
    # Root path → login page
    path('', RedirectView.as_view(pattern_name='login', permanent=False), name='home'),
    path('landing/', landing_view, name='landing'),
]
