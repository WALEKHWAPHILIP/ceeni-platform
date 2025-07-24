# ------------------------------------------------------------------------------
# APP CONFIG: User Profiles — Demographics, Interests, and Civic Preferences
# ------------------------------------------------------------------------------

from django.apps import AppConfig

class UserProfilesConfig(AppConfig):
    """
    AppConfig for user_profiles — handles civic, demographic, and interest data
    tied to CustomUser via UserProfile.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.user_profiles'

    def ready(self):
        # Import signal handlers when app is ready — critical for profile auto-creation
        import apps.user_profiles.signals
