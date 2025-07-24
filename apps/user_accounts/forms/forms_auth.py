# =======================
# Django & Third-Party Imports
# =======================
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

# =======================
# Local Application Imports
# =======================
from ..models import CustomUser
from apps.common.validators.identity import (
    validate_phone_e164,
    validate_nickname,
)


# ===========================================
# RegistrationForm: Handles user sign-up logic
# ===========================================
class RegistrationForm(forms.ModelForm):
    """
    User registration form for creating a new account.
    Includes E.164 phone number validation, nickname checks, 
    and password strength confirmation.
    """

    # Validates phone number in E.164 format (e.g., +254712345678)
    phone_number = forms.CharField(
        help_text="Must be valid. Format: +254712345678 - used for OTP and login security.",
        validators=[validate_phone_e164],
        widget=forms.TextInput(attrs={
            "class": "input input-bordered w-full",
            "placeholder": "e.g. +254712345678"
        })
    )

    # Nickname with custom validation (length and uniqueness)
    nickname = forms.CharField(
        min_length=3,
        max_length=10,
        validators=[validate_nickname],
        widget=forms.TextInput(attrs={
            "class": "input input-bordered w-full",
            "placeholder": "Pick a unique nickname"
        })
    )

    # Primary password field
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "input input-bordered w-full",
            "placeholder": "Create a strong password"
        }),
        min_length=12,
        help_text="Use at least 12 characters. Avoid common passwords."
    )

    # Confirmation password field
    password_confirm = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            "class": "input input-bordered w-full",
            "placeholder": "Repeat your password"
        }),
        help_text="Repeat the password to confirm."
    )

    # Placeholder for CAPTCHA (future enhancement)
    captcha = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "input input-bordered w-full",
            "placeholder": "Enter the text you see above"
        }),
        help_text="This protects against bots."
    )

    class Meta:
        model = CustomUser
        fields = ['phone_number', 'nickname', 'password']

    def clean(self):
        """
        Custom clean method to ensure password fields match.
        """
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error("password_confirm", "Passwords do not match.")

    def clean_password(self):
        """
        Validates password using Django’s built-in password validators.
        """
        password = self.cleaned_data.get('password')
        if password:
            validate_password(password)
        return password





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
        self.fields["username"].help_text = "Use the phone number you registered with (E.164 format)."
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
