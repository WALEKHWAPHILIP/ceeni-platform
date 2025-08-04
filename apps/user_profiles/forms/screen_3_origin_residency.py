# apps/user_profiles/forms/screen_3_origin_residency.py

from django import forms
from django_countries.widgets import CountrySelectWidget
from apps.user_profiles.models import UserProfile

# Shared Tailwind Select styling
BASE_SELECT_CLS = (
    "select select-bordered w-full rounded-lg "
    "transition duration-300 ease-in-out shadow-sm "
    "focus:outline-none focus:ring-2 focus:ring-green-600"
)

class Screen3OriginResidencyForm(forms.ModelForm):
    """
    Step 3: Origin & Residency Form
    - Captures ancestral county, current country, and residency type.
    - Uses a shared BASE_SELECT_CLS for all select widgets.
    - Adds friendly empty labels for each ModelChoiceField.
    """

    class Meta:
        model = UserProfile
        fields = [
            'county_of_origin',
            'current_country_of_residence',
            'residency_type',
        ]
        widgets = {
            'county_of_origin': forms.Select(attrs={'class': BASE_SELECT_CLS}),
            'current_country_of_residence': CountrySelectWidget(attrs={'class': BASE_SELECT_CLS}),
            'residency_type': forms.Select(attrs={'class': BASE_SELECT_CLS}),
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
        for name, field in self.fields.items():
            # All fields are required
            field.required = True
            # For ModelChoiceFields, set a clear empty_label
            if isinstance(field, forms.ModelChoiceField):
                field.empty_label = f"Select {field.label.lower()}"
