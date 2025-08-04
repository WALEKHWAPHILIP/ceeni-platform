# apps/user_accounts/urls.py

from django.urls import path

# ─────────────────────────────────────────────────────────────
# Modular View Imports (logical separation of concerns)
# ─────────────────────────────────────────────────────────────
from .views.login import CustomLoginView
from .views.logout import CustomLogoutView
from .views.signup import (
    signup_entry,         # Handles routing logic if user is already logged in
    register,             # Displays and processes the actual registration form
    logout_then_signup    # Logs out current user then redirects to register
)

app_name = "user_accounts"  # Enables namespaced URL resolution (e.g. user_accounts:login)

urlpatterns = [

    # ─────────────────────────────────────────────────────────────
    # User Authentication Routes
    # ─────────────────────────────────────────────────────────────

    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),

    # ─────────────────────────────────────────────────────────────
    # User Registration & Switch-Account Logic
    # ─────────────────────────────────────────────────────────────

    # Public-facing entry point for signup — includes auth check
    path("signup/", signup_entry, name="signup_entry"),

    # Actual registration form (used after logout or entry pass)
    path("signup/new/", register, name="register"),

    # Log out current user, then redirect to signup form
    path("signup/switch/", logout_then_signup, name="logout_then_signup"),

    # ─────────────────────────────────────────────────────────────
    # (Planned) Password Reset & Profile Management
    # ─────────────────────────────────────────────────────────────

    # path("password-reset/", ResetPasswordView.as_view(), name="password_reset"),
    # path("password-reset-confirm/<uidb64>/<token>/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    # path("profile/", ProfileView.as_view(), name="profile"),
]
