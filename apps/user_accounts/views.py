# =======================
# Django Imports
# =======================
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView

# =======================
# Local Application Imports
# =======================
from .forms.forms_auth import (
    RegistrationForm,
    LoginForm,
)
from apps.common.utils.ip_tracker import get_client_ip


# ───────────────────────────────────────────────────────────────────────────────
# FILE: apps/user_accounts/views.py
# PURPOSE:
#   - Handles user authentication workflows: register, login, logout.
#   - Integrates with Django’s built-in auth system.
# ───────────────────────────────────────────────────────────────────────────────

# ------------------------------------------------------------------------------
# View: User Registration
# ------------------------------------------------------------------------------
def register(request):
    """
    Handles new user registration.
    Accepts POST data via RegistrationForm and creates a new user.
    Also captures the IP address and stores it in the related UserProfile.
    """
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hash password
            user.save()

            # Log the user in
            login(request, user)

            # Capture real client IP using utility
            ip = get_client_ip(request)
            try:
                profile = user.userprofile
                profile.registration_ip = ip
                profile.save()
            except Exception:
                pass  # Skip silently if UserProfile not found

            return render(request, "user_accounts/registration_success.html", {
                "username": user.username
            })
    else:
        form = RegistrationForm()

    return render(request, "user_accounts/register.html", {"form": form})


# ------------------------------------------------------------------------------
# View: Custom Login
# ------------------------------------------------------------------------------
class CustomLoginView(LoginView):
    """
    Displays the login form and authenticates the user using phone number and password.
    Uses a custom LoginForm for validation and styling.
    Redirects to first profile screen on success.
    """
    template_name = "user_accounts/login.html"
    authentication_form = LoginForm

    def get_success_url(self):
        user = self.request.user

        if not hasattr(user, "userprofile"):
            return reverse_lazy("user_profiles:screen_1")

        profile = user.userprofile
        if profile.has_required_profile_fields():
            return reverse_lazy("dashboard")  # Replace with your real dashboard route
        else:
            return reverse_lazy("user_profiles:profile_checker")


# ------------------------------------------------------------------------------
# View: Custom Logout
# ------------------------------------------------------------------------------
class CustomLogoutView(LogoutView):
    """
    Logs the user out and redirects them to the login page (or homepage).
    """
    next_page = "/"  # Redirect after logout
