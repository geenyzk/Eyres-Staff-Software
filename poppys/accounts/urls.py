from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('pending/', views.pending, name='pending'),
    path('contact_admin/', views.contact_admin, name='contact_admin'),  # New URL pattern
]
