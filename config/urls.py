# =======================
# Django Imports
# =======================
from django.contrib import admin
from django.urls import path, include

# =======================
# Static & Media Handling
# =======================
from django.conf import settings
from django.conf.urls.static import static

# ───────────────────────────────────────────────────────────────────────────────
# FILE: config/urls.py
# PURPOSE:
#   - Root URL configuration for the CEENI Platform.
#   - Centralized routing for admin, user accounts, profiles, landing pages, etc.
# ───────────────────────────────────────────────────────────────────────────────

urlpatterns = [

    # --------------------------------------------------------------------------
    # Django Admin Panel
    # --------------------------------------------------------------------------
    # Admin interface for superusers to manage the platform
    path('admin/', admin.site.urls),

    # --------------------------------------------------------------------------
    # User Profile Autocomplete Routing
    # --------------------------------------------------------------------------
    # AJAX autocomplete views (e.g. country ➝ region ➝ district ➝ location)
    # Used in user profile forms via Select2 widgets
    path("profiles/autocomplete/", include("apps.user_profiles.urls_autocomplete")),

    # --------------------------------------------------------------------------
    # HTMX User Profiles Routing
    # --------------------------------------------------------------------------
    # Handles HTMX-based endpoints for user profile interactivity (e.g. inline
    # updates, conditional field rendering, async validation, etc.)
    path("htmx/user-profiles/", include("apps.user_profiles.urls_htmx")),

    # --------------------------------------------------------------------------
    # User Accounts App Routing
    # --------------------------------------------------------------------------
    # Handles user registration, login, logout, password reset, etc.
    path("accounts/", include("apps.user_accounts.urls")),

    # --------------------------------------------------------------------------
    # Progressive User Profile Registration Routing
    # --------------------------------------------------------------------------
    # Handles screen-by-screen progressive profile creation
    # Step 1–6: basic-info ➝ location ➝ origin ➝ civic-interests ➝ etc.
    path("profile/register/", include("apps.user_profiles.urls")),

    # --------------------------------------------------------------------------
    # Landing Page App Routing
    # --------------------------------------------------------------------------
    # Routes root domain (`/`) to the public-facing landing app
    # Example: homepage, about, contact, etc.
    path('', include("apps.landing.urls")),
]

# ==============================================================================
# MEDIA FILES IN DEVELOPMENT
# ==============================================================================
# This allows media (e.g., uploaded profile pictures) to be served directly
# via Django's dev server. Not suitable for production use.
# ------------------------------------------------------------------------------
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
