# apps/user_profiles/forms/screen_6_referral_source.py

from django import forms
from apps.user_profiles.models import UserProfile

# Shared Tailwind Select styling
BASE_SELECT_CLS = (
    "select select-bordered w-full rounded-lg "
    "transition duration-300 ease-in-out shadow-sm "
    "focus:outline-none focus:ring-2 focus:ring-green-600"
)

class Screen6ReferralSourceForm(forms.ModelForm):
    """
    Step 6: Referral Source
    - Captures how the user heard about CEENI.
    """

    class Meta:
        model = UserProfile
        fields = ['referral_source']
        widgets = {
            'referral_source': forms.Select(attrs={'class': BASE_SELECT_CLS}),
        }
        labels = {
            'referral_source': "How did you hear about CEENI?",
        }
        help_texts = {
            'referral_source': "Let us know how you first learned about our platform.",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        field = self.fields['referral_source']
        field.required = True
        # Show a placeholder rather than a blank first choice
        field.empty_label = f"Select {field.label.lower()}"
