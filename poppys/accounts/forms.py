from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("full_name", "username", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-600 focus:outline-none'
            })

    def save(self, commit=True):
        # Base UserCreationForm behavior: set a hashed password
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])  # ensure password is set
        # Create users as inactive until approved
        user.is_active = False
        if commit:
            user.save()
        return user


class PendingAwareAuthenticationForm(AuthenticationForm):
    """
    Authentication form that does not block inactive users at form validation
    time. This allows the view to detect inactivity and redirect to a
    pending-approval page instead of showing a generic error.
    """

    def confirm_login_allowed(self, user):
        # Override default behavior that rejects inactive users.
        # The view will handle redirecting inactive users to the pending page.
        return
