from django.apps import AppConfig  # Import Django's application configuration base class

# Configuration class for the 'documents' app
class CeeniDocumentsConfig(AppConfig):
    # Specifies the type of primary key field to use by default for models in this app
    default_auto_field = "django.db.models.BigAutoField"
    
    # Full Python path to the application (as listed in INSTALLED_APPS)
    name = "apps.ceeni_documents"
    
    # Human-readable name for the app, shown in the Django admin and elsewhere
    verbose_name = "Documents"
