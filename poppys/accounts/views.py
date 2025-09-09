from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import PendingAwareAuthenticationForm
from django.contrib import messages
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm

# Create your views here.

def login_view(request):
    form = PendingAwareAuthenticationForm(request, data=request.POST or None)

    if request.method == 'POST':
        # Explicitly catch inactive-but-correct-credentials before form validation
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            User = get_user_model()
            try:
                candidate = User.objects.get(username=username)
            except User.DoesNotExist:
                candidate = None
            if candidate and not candidate.is_active and candidate.check_password(password):
                messages.warning(request, 'Your account is not active yet. Please contact the administrator.')
                return redirect('pending')

        if form.is_valid():
            user = form.get_user()

            if not user.is_active:
                messages.warning(request, 'Your account is not active yet. Please contact the administrator.')
                return redirect('pending')

            login(request, user)
            return redirect('landing')
        else:
            messages.error(request, 'Invalid credentials.')

    return render(request, 'accounts/login.html', {'form': form})



def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully. Please log in.')
            return redirect('login')  # Make sure 'login' URL name is correct
        else:
            messages.error(request, 'Error creating account. Please check the form.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login') # Replace with login URL

def pending(request):
    return render(request, 'accounts/pending.html')
 
