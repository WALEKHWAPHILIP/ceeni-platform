# apps/user_accounts/forms/auth_login.py

# =======================
# Django & Third-Party Imports
# =======================
from django import forms
from django.contrib.auth.forms import AuthenticationForm

# =======================
# Local Application Imports
# =======================
from apps.common.validators.identity import (
    validate_phone_e164,
)



# ===========================================
# LoginForm: Auth via phone number + password
# ===========================================
class LoginForm(AuthenticationForm):
    """
    Custom login form using phone number and password with CEENI styling.
    Extends Django's built-in AuthenticationForm with:
        - E.164 phone validation
        - Tailwind styling
        - "Remember me" functionality
    """

    # Optional checkbox to maintain session across restarts
    remember_me = forms.BooleanField(
        required=False,
        label="Keep me logged in",
        widget=forms.CheckboxInput(attrs={
            "class": "checkbox"
        })
    )

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request=request, *args, **kwargs)

        # Override username to be phone number
        self.fields["username"].label = "Phone Number"
        self.fields["username"].help_text = "Use the phone number you registered with (E.164 format say eg. +254712345678)"
        self.fields["username"].widget.attrs.update({
            "class": "input input-bordered w-full",
            "placeholder": "+254712345678",
            "autofocus": "autofocus"
        })
        self.fields["username"].validators = [validate_phone_e164]

        # Style the password field
        self.fields["password"].widget.attrs.update({
            "class": "input input-bordered w-full",
            "placeholder": "Enter your password"
        })
        self.fields["password"].help_text = "Your password is never shared."
