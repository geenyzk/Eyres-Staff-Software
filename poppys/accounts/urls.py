from django.urls import path
from . import views

url_patterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.logout_view, name='signup'),
    path('logout/', views.register_view, name='logout'),
]
