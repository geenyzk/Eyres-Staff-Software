from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import PendingAwareAuthenticationForm
from django.contrib import messages
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm
from django.core.mail import send_mail
from django.conf import settings

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
                # Save pending identity for the contact_admin view
                request.session['pending_identity'] = {
                    'username': candidate.username,
                    'email': candidate.email,
                    'full_name': getattr(candidate, 'full_name', ''),
                }
                return redirect('pending')

        if form.is_valid():
            user = form.get_user()

            if not user.is_active:
                messages.warning(request, 'Your account is not active yet. Please contact the administrator.')
                request.session['pending_identity'] = {
                    'username': user.username,
                    'email': user.email,
                    'full_name': getattr(user, 'full_name', ''),
                }
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


def contact_admin(request):
    """Send an activation request email to admins for the pending user.
    Works for users who aren’t logged in by using the identity stored in
    session during the pending redirect. Falls back to request.user if
    available.
    """
    if request.method != 'POST':
        messages.error(request, 'Invalid request.')
        return redirect('pending')

    identity = request.session.get('pending_identity') or {}
    if request.user.is_authenticated:
        identity = {
            'username': getattr(request.user, 'username', identity.get('username')),
            'email': getattr(request.user, 'email', identity.get('email')),
            'full_name': getattr(request.user, 'full_name', identity.get('full_name', '')),
        }

    if not identity.get('username'):
        messages.error(request, 'No pending user information found. Please log in again.')
        return redirect('login')

    subject = 'Activation Request: Pending User'
    message = (
        f"A user has requested activation.\n\n"
        f"Full name: {identity.get('full_name') or 'N/A'}\n"
        f"Username: {identity.get('username')}\n"
        f"Email: {identity.get('email') or 'N/A'}\n"
    )

    recipient_list = list(getattr(settings, 'ADMIN_EMAILS', []) or [])
    fallback_from = getattr(settings, 'DEFAULT_FROM_EMAIL', '')
    if not recipient_list and fallback_from:
        recipient_list = [fallback_from]

    if not recipient_list:
        messages.error(request, 'Admin email is not configured. Please set ADMIN_EMAILS.')
        return redirect('pending')

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=fallback_from or None,
            recipient_list=recipient_list,
            fail_silently=False,
        )
        backend_used = getattr(settings, 'EMAIL_BACKEND', '')
        if 'console' in backend_used:
            messages.success(request, 'Request sent (printed to console backend). Configure SMTP to send real emails.')
        else:
            messages.success(request, 'Your activation request has been emailed to the admin.')
    except Exception as e:
        messages.error(request, f'Could not send email: {e}')

    return redirect('pending')
 
