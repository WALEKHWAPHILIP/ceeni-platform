# Import all base settings to inherit common configurations
from .base import *

# Disable debug mode for production to avoid leaking sensitive info
DEBUG = False

# Specify the allowed hosts for your production deployment
# Replace with your actual domain(s) to prevent Host header attacks
ALLOWED_HOSTS = ["ceeni.walsoftai.com"]

# Database configuration for production environment using PostgreSQL
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",  # Use PostgreSQL backend
        "NAME": os.getenv("DB_NAME"),               # Database name from environment variables
        "USER": os.getenv("DB_USER"),               # Database username from environment variables
        "PASSWORD": os.getenv("DB_PASSWORD"),       # Password securely stored in environment
        "HOST": os.getenv("DB_HOST", "localhost"),  # DB host with fallback to localhost
        "PORT": os.getenv("DB_PORT", "5432"),       # DB port with fallback to default PostgreSQL port
    }
}
