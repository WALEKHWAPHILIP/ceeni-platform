from django.apps import AppConfig


# -------------------------------
# App Configuration for Common App
# -------------------------------
class CommonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'

    name = 'apps.common'

    # Optional: Give a human-readable name for the admin interface
    verbose_name = "Shared Core Logic"
