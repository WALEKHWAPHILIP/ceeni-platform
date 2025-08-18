# apps/user_accounts/forms/auth_registration.py

# =======================
# Django & Third-Party Imports
# =======================
from django import forms
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
from apps.ceeni_captcha.forms.captcha_mixin import CaptchaFieldMixin  # ✅ Import the reusable captcha logic


# ===========================================
# RegistrationForm: Handles user sign-up logic
# ===========================================
class RegistrationForm(CaptchaFieldMixin, forms.ModelForm):
    """
    CEENI Registration Form

    Combines:
    - Phone + Nickname + Password fields
    - Civic & jumbled captcha validation (via mixin)
    """

    phone_number = forms.CharField(
        help_text="Must be valid. Format: +254712345678. This number will be used for OTP verification and login security - please use a number you own and can easily remember.",
        validators=[validate_phone_e164],
        widget=forms.TextInput(attrs={
            "class": "input input-bordered w-full",
            "placeholder": "e.g. +254712345678"
        })
    )

    nickname = forms.CharField(
        min_length=3,
        max_length=10,
        help_text=(
            "Choose a short, unique name (3-10 characters). "
            "This name will represent you on the Ceeni platform - make it memorable. "
            "Example: JB Baraka. "
            "We’ll automatically append system-generated characters to ensure global uniqueness "
            "(e.g., jb-baraka-t4c754)."
        ),
        validators=[validate_nickname],
        widget=forms.TextInput(attrs={
            "class": "input input-bordered w-full",
            "placeholder": "e.g. JB Baraka"
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "input input-bordered w-full",
            "placeholder": "Create a strong password"
        }),
        min_length=12,
        help_text="Use at least 12 characters. Avoid common passwords."
    )

    password_confirm = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            "class": "input input-bordered w-full",
            "placeholder": "Repeat your password"
        }),
        help_text="Repeat the password to confirm."
    )

    class Meta:
        model = CustomUser
        fields = ['phone_number', 'nickname', 'password']

    def __init__(self, *args, **kwargs):
        """
        Extract the request object to pass to the CaptchaFieldMixin.
        This enables session-based randomization and validation.
        """
        self.request = kwargs.pop('request', None)
        super().__init__(*args, request=self.request, **kwargs)

    def clean(self):
        """
        Ensure that password and confirmation match.
        Captcha validation is handled by the mixin.
        """
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error("password_confirm", "Passwords do not match.")

        return cleaned_data

    def clean_password(self):
        """
        Use Django’s built-in password validation logic (min length, strength, etc).
        """
        password = self.cleaned_data.get('password')
        if password:
            validate_password(password)
        return password
