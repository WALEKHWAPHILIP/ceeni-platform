from django import forms
from apps.user_profiles.models import UserProfile


class Screen4CivicInterestsForm(forms.ModelForm):
    """
    Step 4: Civic Interests & Participation
    - Captures user civic interests and engagement familiarity.
    - Uses checkboxes and radio buttons with proper coercion to booleans.
    """

    YES_NO_CHOICES = [
        (True, "Yes"),
        (False, "No"),
    ]

    has_voted_before = forms.TypedChoiceField(
        label="Have you voted before?",
        choices=YES_NO_CHOICES,
        coerce=lambda x: x in [True, "True", "true", "1", 1],
        widget=forms.RadioSelect(attrs={"class": "flex flex-col gap-2"}),
        required=True,
    )

    knows_voting_process = forms.TypedChoiceField(
        label="Do you understand the voting process?",
        choices=YES_NO_CHOICES,
        coerce=lambda x: x in [True, "True", "true", "1", 1],
        widget=forms.RadioSelect(attrs={"class": "flex flex-col gap-2"}),
        required=True,
    )

    class Meta:
        model = UserProfile
        fields = ['civic_interest_areas', 'has_voted_before', 'knows_voting_process']

        widgets = {
            'civic_interest_areas': forms.CheckboxSelectMultiple(attrs={
                "class": "space-y-2"
            }),
        }

        labels = {
            'civic_interest_areas': "What civic topics interest you?",
        }

        help_texts = {
            'civic_interest_areas': "Pick 1 to 5 topics you care about (e.g. Health, Youth, Corruption).",
            'has_voted_before': "This helps us understand civic familiarity.",
            'knows_voting_process': "Used to guide education and outreach efforts.",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['civic_interest_areas'].required = True

    def clean_civic_interest_areas(self):
        interests = self.cleaned_data.get('civic_interest_areas')
        if interests and interests.count() > 5:
            raise forms.ValidationError("You can select up to 5 civic interests.")
        return interests
