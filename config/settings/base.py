"""
Base settings for CEENI Platform (Django 5.2+)

Docs:
- https://docs.djangoproject.com/en/5.2/ref/settings/
"""

import os
from pathlib import Path

# ------------------------------------------------------------------------------
# PATHS
# ------------------------------------------------------------------------------

# BASE_DIR resolves to the project root (three levels up from this file)
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent

# CSV_DATA_DIR points to the directory where all CSV data files will be stored
# Used for data ingestion, export, or temp file generation
CSV_DATA_DIR = BASE_DIR / "data" / "csv"


# ------------------------------------------------------------------------------
# CORE CONFIGURATION (Environment-specific values are overridden in dev/prod)
# ------------------------------------------------------------------------------
SECRET_KEY = os.getenv("SECRET_KEY", "INSECURE-DEV-KEY")
DEBUG = False
ALLOWED_HOSTS = []

# ------------------------------------------------------------------------------
# APPLICATION DEFINITIONS
# ------------------------------------------------------------------------------
INSTALLED_APPS = [
    # Django core
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # ------------------------------------------------------------------------------  
    # Third-Party Apps  
    # ------------------------------------------------------------------------------  
    'dal',                                  # Django Autocomplete Light core  
    'dal_select2',                          # Select2 widget support (beautiful dropdowns)  
    'django_countries',                     # Provides ISO 3166-1 country field support with translations
    'widget_tweaks',                        # Enables template-level form field customization using {% render_field %}  


    # ------------------------------------------------------------------------------  
    # CEENI Custom Apps  
    # ------------------------------------------------------------------------------  
    'common.apps.CommonConfig',                  # Shared logic: reusable models, validators, filters
    'user_accounts.apps.UserAccountsConfig',     # Handles user registration, login, authentication, roles, and permissions
    'user_profiles.apps.UserProfilesConfig',     # Manages user profile data (e.g. bio, avatar, preferences, demographics)
    'landing.apps.LandingConfig',                # Landing page views, templates, public homepage, and static content
    'dashboard.apps.DashboardConfig',            # Dashboard landing & post-onboarding views

]

# ────────────────────────────────────────────────────────────────────────────────
# TAILWIND CSS FRAMEWORK INTEGRATION
# ────────────────────────────────────────────────────────────────────────────────
# PURPOSE:
#     - Integrates Tailwind CSS into the Django build and rendering pipeline.
#     - Supports hot-reloading via unified Tailwind CLI and Django dev server.
#     - Ensures clean modular separation of frontend logic in a dedicated theme app.
#
# DEPENDENCIES:
#     - `django-tailwind` (v4+ recommended)
#     - Tailwind theme initialized via `python manage.py tailwind init apps.theme`
#
# NOTES:
#     - The theme app should be located in `apps/theme`
#     - Compatible with modern Tailwind v4+ (no JS config needed)
# ────────────────────────────────────────────────────────────────────────────────

# Tailwind App Loader
# This tells Django-Tailwind which app contains the Tailwind configuration and assets.
# IMPORTANT: This must match the name given when initializing the theme app.
TAILWIND_APP_NAME = 'apps.theme'

# Tailwind and Theme App
# These must be declared in INSTALLED_APPS to enable Tailwind compilation and template tag loading.
INSTALLED_APPS += [
    'tailwind',                # Tailwind CSS integration manager for Django
    'apps.theme',              # Modular frontend theme app (holds tailwind.config and styles)
]



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'

# ------------------------------------------------------------------------------
# TEMPLATES
# ------------------------------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                # CEENI user context processor
                'apps.common.context_processors.ceeni_user_data.global_user_data',
            ],
        },
    },
]

# ------------------------------------------------------------------------------
# DATABASE (Default: SQLite — overridden in dev/prod)
# ------------------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / "db.sqlite3",
    }
}


# ------------------------------------------------------------------------------
# PASSWORD VALIDATION
# ------------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 12,}},
]

# ------------------------------------------------------------------------------
# I18N & TIMEZONE
# ------------------------------------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Oslo'
USE_I18N = True
USE_TZ = True

# ------------------------------------------------------------------------------
# STATIC / MEDIA
# ------------------------------------------------------------------------------
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ------------------------------------------------------------------------------
# AUTH CONFIGURATION
# ------------------------------------------------------------------------------

# Specify the custom user model to replace Django's default User
AUTH_USER_MODEL = "user_accounts.CustomUser"

# ------------------------------------------------------------------------------
# DEFAULT PRIMARY KEY FIELD TYPE
# ------------------------------------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ------------------------------------------------------------------------------
# LOGGING
# ------------------------------------------------------------------------------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        }
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
}
