# ──────────────────────────────────────────────────────────────────────────
# FILE: apps/user_profiles/forms/screen_3_origin_residency.py
# PURPOSE: Step 3 of CEENI registration – Origin & Residency Info Form
# ──────────────────────────────────────────────────────────────────────────

from django import forms
from apps.user_profiles.models import UserProfile


class Screen3OriginResidencyForm(forms.ModelForm):
    """
    Step 3: Origin & Residency Form
    - Captures ancestral county, current country, and residency type.
    - Tailwind + daisyUI styled.
    """

    class Meta:
        model = UserProfile
        fields = ['county_of_origin', 'current_country_of_residence', 'residency_type']

        widgets = {
            'county_of_origin': forms.Select(attrs={
                "class": "select select-bordered w-full rounded-lg transition shadow-sm focus:outline-none focus:ring-2 focus:ring-green-600",
            }),
            'current_country_of_residence': forms.Select(attrs={
                "class": "select select-bordered w-full rounded-lg transition shadow-sm focus:outline-none focus:ring-2 focus:ring-green-600",
            }),
            'residency_type': forms.Select(attrs={
                "class": "select select-bordered w-full rounded-lg transition shadow-sm focus:outline-none focus:ring-2 focus:ring-green-600",
            }),
        }

        labels = {
            'county_of_origin': "County of Origin",
            'current_country_of_residence': "Current Country",
            'residency_type': "Residency Type",
        }

        help_texts = {
            'county_of_origin': "This may be where you or your family traces roots from.",
            'current_country_of_residence': "Where you currently live. This helps understand diaspora input.",
            'residency_type': "Choose the type of place you live in.",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True
