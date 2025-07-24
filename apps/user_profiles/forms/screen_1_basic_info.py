# ──────────────────────────────────────────────────────────────────────────
# FILE: apps/user_profiles/forms/screen_1_basic_info.py
# PURPOSE: Step 1 of CEENI registration – Basic Info Form
#           Captures age range, gender, and education level.
# ──────────────────────────────────────────────────────────────────────────

from django import forms
from apps.user_profiles.models import UserProfile


class Screen1BasicInfoForm(forms.ModelForm):
    """
    Step 1: Basic Info Form
    - Captures age range, gender, and education level.
    - Uses Tailwind + daisyUI widgets for elegance.
    """

    class Meta:
        model = UserProfile
        fields = ['age_range', 'gender', 'education_level']

        widgets = {
            'age_range': forms.Select(attrs={
                "class": "select select-bordered w-full rounded-lg transition duration-300 ease-in-out shadow-sm focus:outline-none focus:ring-2 focus:ring-green-600",
            }),
            'gender': forms.Select(attrs={
                "class": "select select-bordered w-full rounded-lg transition duration-300 ease-in-out shadow-sm focus:outline-none focus:ring-2 focus:ring-green-600",
            }),
            'education_level': forms.Select(attrs={
                "class": "select select-bordered w-full rounded-lg transition duration-300 ease-in-out shadow-sm focus:outline-none focus:ring-2 focus:ring-green-600",
            }),
        }

        help_texts = {
            'age_range': "Select your age bracket (used only for civic insights).",
            'gender': "Choose how you identify. This informs inclusive representation.",
            'education_level': "Select your highest completed education level.",
        }

        labels = {
            'age_range': "Age Range",
            'gender': "Gender",
            'education_level': "Education Level",
        }

    def __init__(self, *args, **kwargs):
        """
        Custom init to apply consistent placeholder if needed in future.
        """
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True  # All fields on this screen are required
