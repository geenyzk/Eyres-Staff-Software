# core/urls.py
from django.urls import path
from .views import landing_view

urlpatterns = [
    path('landing/', landing_view, name='landing'),
]