# apps > user_profiles > forms > screen_7_confirmation_and_save.py

from django import forms
from apps.user_profiles.models import UserProfile

class Screen7ConfirmationAndSaveForm(forms.ModelForm):
    """
    Step 7: Confirmation & Final Save.
    No additional editable fields—just a submit to finalize onboarding.
    """
    class Meta:
        model = UserProfile
        fields = []  # all data already captured in prior steps
