from django import forms
from apps.common.validators.identity import validate_phone_e164
from apps.user_profiles.models import UserProfile


class Screen5CommunicationForm(forms.ModelForm):
    """
    Step 5: Communication Preferences
    - Explicit opt-in to bill notifications
    - WhatsApp number required ONLY if opted in
    """

    YES_NO_CHOICES = [
        ("", "Please choose"),  # Neutral option to avoid defaulting to Yes
        (True, "Yes"),
        (False, "No"),
    ]

    wants_bill_notifications = forms.TypedChoiceField(
        label="Would you like to receive bill notifications?",
        choices=YES_NO_CHOICES,
        coerce=lambda x: x in [True, "True", "true", "1", 1],
        empty_value=None,
        widget=forms.Select(attrs={
            "class": "select select-bordered w-full rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-green-600"
        }),
        required=True,
    )

    class Meta:
        model = UserProfile
        fields = ["wants_bill_notifications", "whatsapp_opt_in_number"]

        labels = {
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
            "whatsapp_opt_in_number": forms.TextInput(attrs={
                "class": "input input-bordered w-full rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-green-600",
                "placeholder": "+254712345678"
            }),
        }

    def clean_whatsapp_opt_in_number(self):
        """
        Only validate WhatsApp number if user has opted in.
        """
        number = self.cleaned_data.get("whatsapp_opt_in_number")
        wants = self.cleaned_data.get("wants_bill_notifications")

        if wants and not number:
            raise forms.ValidationError(
                "Please provide a WhatsApp number if you opted in for notifications."
            )
        if number:
            validate_phone_e164(number)
        return number
