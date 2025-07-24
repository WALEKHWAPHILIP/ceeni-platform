# ──────────────────────────────────────────────────────────────────────────────
# FILE: apps/user_profiles/forms/screen_5_communication.py
# PURPOSE: Step 5 of CEENI registration – Communication Preferences
# ──────────────────────────────────────────────────────────────────────────────

from django import forms
from apps.user_profiles.models import UserProfile
from apps.common.validators.identity import validate_phone_e164


class Screen5CommunicationForm(forms.ModelForm):
    """
    Step 5: Communication Preferences Only
    - Opt-in to notifications
    - Provide WhatsApp number (optional if opted in)
    """

    class Meta:
        model = UserProfile
        fields = ["wants_bill_notifications", "whatsapp_opt_in_number"]

        labels = {
            "wants_bill_notifications": "Would you like to receive bill notifications?",
            "whatsapp_opt_in_number": "WhatsApp Number for Alerts (Optional)",
        }

        help_texts = {
            "wants_bill_notifications": (
                "Would you like to be notified when major progress is made on the Ethnic Equity and "
                "Public Representation Bill, including voting stages and public debates?"
            ),
            "whatsapp_opt_in_number": (
                "If you've opted in, please provide a valid WhatsApp number in international format (e.g., +254712345678)."
            ),
        }

        widgets = {
            "wants_bill_notifications": forms.Select(choices=[
                ("", "— Select —"),
                (True, "Yes"),
                (False, "No"),
            ], attrs={
                "class": "select select-bordered w-full rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-green-600"
            }),
            "whatsapp_opt_in_number": forms.TextInput(attrs={
                "class": "input input-bordered w-full rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-green-600",
                "placeholder": "+254712345678"
            }),
        }

    def clean_whatsapp_opt_in_number(self):
        """
        Only validate number if user opted in.
        """
        number = self.cleaned_data.get("whatsapp_opt_in_number")
        wants = self.cleaned_data.get("wants_bill_notifications")

        if wants is True and not number:
            raise forms.ValidationError("Please provide a WhatsApp number if you opted in for notifications.")
        if number:
            validate_phone_e164(number)
        return number
