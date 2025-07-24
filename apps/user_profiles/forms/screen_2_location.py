# ──────────────────────────────────────────────────────────────────────────
# FILE: apps/user_profiles/forms/screen_2_location.py
# PURPOSE: Step 2 of CEENI registration – Location Info Form
#          Captures county → constituency → ward in hierarchical order.
# ──────────────────────────────────────────────────────────────────────────

from django import forms
from apps.user_profiles.models import UserProfile


class Screen2LocationForm(forms.ModelForm):
    """
    Step 2: Location Info Form
    - Captures geographic voter location via county → constituency → ward.
    - Styled with Tailwind and daisyUI.
    """

    class Meta:
        model = UserProfile
        fields = ['county', 'constituency', 'ward']

        widgets = {
            'county': forms.Select(attrs={
                "class": "select select-bordered w-full rounded-lg transition duration-300 ease-in-out shadow-sm focus:outline-none focus:ring-2 focus:ring-green-600",
                "hx-get": "/profile/register/htmx/constituencies/",
                "hx-target": "#id_constituency",
                "hx-trigger": "change",
                "name": "county_id"  # HTMX query param
            }),
            'constituency': forms.Select(attrs={
                "class": "select select-bordered w-full rounded-lg transition duration-300 ease-in-out shadow-sm focus:outline-none focus:ring-2 focus:ring-green-600",
                "hx-get": "/profile/register/htmx/wards/",
                "hx-target": "#id_ward",
                "hx-trigger": "change",
                "name": "constituency_id"  # HTMX query param
            }),
            'ward': forms.Select(attrs={
                "class": "select select-bordered w-full rounded-lg transition duration-300 ease-in-out shadow-sm focus:outline-none focus:ring-2 focus:ring-green-600",
            }),
        }


        help_texts = {
            'county': "Select your voting county.",
            'constituency': "Select your constituency (filtered by county).",
            'ward': "Select your ward (filtered by constituency).",
        }

        labels = {
            'county': "County",
            'constituency': "Constituency",
            'ward': "Ward",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True
