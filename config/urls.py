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
    path('admin/', admin.site.urls),

    # --------------------------------------------------------------------------
    # User Profile Autocomplete Routing
    # --------------------------------------------------------------------------
    path("profiles/autocomplete/", include("apps.user_profiles.urls_autocomplete")),

    # --------------------------------------------------------------------------
    # HTMX User Profiles Routing
    # --------------------------------------------------------------------------
    path("profile/", include("apps.user_profiles.urls_htmx")),

    # --------------------------------------------------------------------------
    # HTMX Captcha Reload Routing
    # --------------------------------------------------------------------------
    # Handles HTMX partial reloads of civic captcha questions (for verification)
    path("htmx/captcha/", include("apps.ceeni_captcha.urls_htmx", namespace="ceeni_captcha")),

    # --------------------------------------------------------------------------
    # User Accounts App Routing
    # --------------------------------------------------------------------------
    path("accounts/", include("apps.user_accounts.urls")),

    # --------------------------------------------------------------------------
    # Progressive User Profile Registration Routing
    # --------------------------------------------------------------------------
    path("profile/register/", include("apps.user_profiles.urls")),

    # --------------------------------------------------------------------------
    # CEENI Documents App Routing
    # --------------------------------------------------------------------------
    # Routes all URLs starting with /documents/ to the ceeni_documents app.
    # This handles document ingestion, retrieval, search, etc.
    path("documents/", include("apps.ceeni_documents.urls", namespace="ceeni_documents")),

    # --------------------------------------------------------------------------
    # Landing Page App Routing
    # --------------------------------------------------------------------------
    path('', include("apps.landing.urls")),

    # --------------------------------------------------------------------------
    # Dashboard App Routing
    # --------------------------------------------------------------------------
    path('dashboard/', include('apps.dashboard.urls', namespace='dashboard')),
]

# ==============================================================================
# MEDIA FILES IN DEVELOPMENT
# ==============================================================================
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
