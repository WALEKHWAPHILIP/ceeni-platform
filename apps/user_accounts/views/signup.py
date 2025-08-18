"""
apps/user_accounts/views/signup.py

Handles user registration flow for CEENI Platform:
- Renders the registration form with captcha support
- Validates and creates new users
- Logs them in immediately
- Captures IP address and stores it in the user's profile
- Prevents duplicate signup by already authenticated users
- Supports “switch account” logic via logout-then-register
"""

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.views.decorators.http import require_http_methods
from django.urls import reverse

from ..forms.auth_registration import RegistrationForm
from apps.common.utils.ip_tracker import get_client_ip


@require_http_methods(["GET", "POST"])
def register(request):
    """
    Handles GET and POST requests for user registration.

    POST:
        - Validates submitted form (including captcha)
        - Creates user and sets password securely
        - Logs user in and stores IP on the user profile
        - Redirects to a civic-themed success screen

    GET:
        - Displays the registration form
    """
    if request.method == "POST":
        form = RegistrationForm(request.POST, request=request)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()

            # Log the user in
            login(request, user)

            # Store client IP on user profile
            ip = get_client_ip(request)
            try:
                profile = user.userprofile
                profile.registration_ip = ip
                profile.save()
            except user.userprofile.RelatedObjectDoesNotExist:
                pass

            return render(
                request,
                "user_accounts/registration_success.html"
                # User data provided via context processor: ceeni_user, ceeni_profile
            )
    else:
        form = RegistrationForm(request=request)

    return render(request, "user_accounts/signup.html", {"form": form})


@require_http_methods(["GET"])
def signup_entry(request):
    """
    Acts as an entry point to the registration flow.

    If a user is already logged in, we show them a confirmation screen
    explaining they must log out to create a new account.
    """
    if request.user.is_authenticated:
        return render(request, "user_accounts/already_logged_in_signup.html")
    return redirect("user_accounts:register")


@require_http_methods(["GET"])
def logout_then_signup(request):
    """
    Logs out the current user and redirects back to the registration form.

    Useful when someone wants to sign up a second user on the same device.
    """
    logout(request)
    return redirect("user_accounts:register")
