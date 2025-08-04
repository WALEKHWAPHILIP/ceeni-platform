# apps/user_profiles/forms/screen_2_location.py

from django import forms
from django.urls import reverse_lazy
from apps.user_profiles.models import UserProfile


class Screen2LocationForm(forms.ModelForm):
    """
    Step 2: Location Info Form
    HTMX attributes are entirely on the form’s widgets so the template
    just loops over form fields and gets dynamic loading “for free.”
    """

    class Meta:
        model = UserProfile
        fields = ['county', 'constituency', 'ward']
        widgets = {
            'county': forms.Select(attrs={
                'class': (
                    'select select-bordered w-full rounded-lg '
                    'transition duration-300 ease-in-out shadow-sm '
                    'focus:outline-none focus:ring-2 focus:ring-green-600'
                ),
                # When county changes, ask our HTMX endpoint for constituencies
                'hx-get': reverse_lazy('user_profiles:htmx_constituencies'),
                'hx-target': '#id_constituency',
                'hx-trigger': 'change',
                'hx-include': 'this',
            }),
            'constituency': forms.Select(attrs={
                'class': (
                    'select select-bordered w-full rounded-lg '
                    'transition duration-300 ease-in-out shadow-sm '
                    'focus:outline-none focus:ring-2 focus:ring-green-600'
                ),
                # When constituency changes, ask for wards
                'hx-get': reverse_lazy('user_profiles:htmx_wards'),
                'hx-target': '#id_ward',
                'hx-trigger': 'change',
                'hx-include': 'this',
            }),
            'ward': forms.Select(attrs={
                'class': (
                    'select select-bordered w-full rounded-lg '
                    'transition duration-300 ease-in-out shadow-sm '
                    'focus:outline-none focus:ring-2 focus:ring-green-600'
                ),
            }),
        }
        labels = {
            'county': 'County',
            'constituency': 'Constituency',
            'ward': 'Ward',
        }
        help_texts = {
            'county': 'Select your voting county.',
            'constituency': 'Filtered by county selection.',
            'ward': 'Filtered by constituency selection.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # All fields required
        for field in self.fields.values():
            field.required = True
