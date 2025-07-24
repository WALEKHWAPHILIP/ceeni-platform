# ------------------------------------------------------------------------------
# SIGNALS: Automatically create UserProfile when a new CustomUser is registered
# ------------------------------------------------------------------------------

from django.db.models.signals import post_save
from django.dispatch import receiver
import phonenumbers

from apps.user_accounts.models import CustomUser
from .models.profile import UserProfile

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Auto-create a UserProfile immediately after a CustomUser is created.
    Also attempts to infer the country from the phone number using phonenumbers lib.
    """
    if created and not hasattr(instance, "userprofile"):
        country = "undetermined"

        # Try to detect country code from phone number
        try:
            parsed = phonenumbers.parse(instance.phone_number, None)
            country = phonenumbers.region_code_for_number(parsed) or "undetermined"
        except:
            pass  # Fallback to 'undetermined' if parsing fails

        # Create the associated UserProfile with country info
        UserProfile.objects.create(
            user=instance,
            country_from_phone_code=country
        )
