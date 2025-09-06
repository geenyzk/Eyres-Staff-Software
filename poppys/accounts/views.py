from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

# Create your views here.

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard') # Replace with dashboard URL 
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'accounts/login.html')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully')
            return redirect('login') # Replace with login URL
        else:
            messages.error(request, 'Error creating account')
    return render(request, 'accounts/signup.html', {'form': UserCreationForm()})

def logout_view(request):
    logout(request)
    return redirect('login') # Replace with login URL

