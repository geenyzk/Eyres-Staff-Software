# core/admin.py
from django.contrib import admin
from .models import Order, Sale

admin.site.register(Order)
admin.site.register(Sale)