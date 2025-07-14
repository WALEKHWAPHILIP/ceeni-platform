# ─────────────────────────────────────────────────────────────
# Load Environment Variables Early (before base settings)
# ─────────────────────────────────────────────────────────────

from dotenv import load_dotenv
import os

load_dotenv()  # Loads .env file into os.environ before any other settings

# ─────────────────────────────────────────────────────────────
# Import Base Settings (modular inheritance)
# ─────────────────────────────────────────────────────────────

from .base import *

# ─────────────────────────────────────────────────────────────
# 🛠 Development Environment Overrides
# ─────────────────────────────────────────────────────────────

DEBUG = True                              # Enable Django debug mode (dev only)
ALLOWED_HOSTS = ["*"]                     # Allow all hosts (not secure for prod)

# ─────────────────────────────────────────────────────────────
# PostgreSQL Database Configuration for Development
# ─────────────────────────────────────────────────────────────

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",        # Use PostgreSQL backend
        "NAME": os.getenv("DB_NAME"),                     # Database name from .env
        "USER": os.getenv("DB_USER"),                     # DB user from .env
        "PASSWORD": os.getenv("DB_PASSWORD"),             # Password from .env
        "HOST": os.getenv("DB_HOST", "localhost"),        # Hostname (default: localhost)
        "PORT": os.getenv("DB_PORT", "5432"),             # Port (default: 5432)
    }
}
