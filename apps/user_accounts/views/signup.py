"""
apps/user_accounts/views/signup.py

Handles user registration flow for CEENI Platform:
- Renders the registration form
- Validates and creates new users
- Logs them in and captures IP address
- Prevents duplicate signup by already authenticated users
- Supports “switch account” logic via logout-then-register
"""

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.views.decorators.http import require_http_methods
from django.urls import reverse

from ..forms.forms_auth import RegistrationForm
from apps.common.utils.ip_tracker import get_client_ip


@require_http_methods(["GET", "POST"])
def register(request):
    """
    Handles GET/POST for the registration form.

    On successful registration:
    - Creates user account and hashes password
    - Logs the user in immediately
    - Captures and stores client IP on user profile
    - Renders a civic-themed success page
    """
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()

            # Log the user in
            login(request, user)

            # Capture and store client IP
            ip = get_client_ip(request)
            try:
                profile = user.userprofile
                profile.registration_ip = ip
                profile.save()
            except user.userprofile.RelatedObjectDoesNotExist:
                pass  # Profile auto-created via signal or elsewhere

            return render(
                request,
                "user_accounts/registration_success.html",
                {"username": user.username},
            )
    else:
        form = RegistrationForm()

    return render(request, "user_accounts/signup.html", {"form": form})


@require_http_methods(["GET"])
def signup_entry(request):
    """
    Gatekeeper for the /signup/ route.

    If user is already logged in, show a switch-account confirmation page.
    If not, redirect to the main register() view.
    """
    if request.user.is_authenticated:
        return render(request, "user_accounts/already_logged_in_signup.html")
    return redirect("user_accounts:register")


@require_http_methods(["GET"])
def logout_then_signup(request):
    """
    Logs out current user and redirects to the registration view.

    Used when a logged-in user chooses to switch accounts
    and create a new one from a shared device.
    """
    logout(request)
    return redirect("user_accounts:register")
