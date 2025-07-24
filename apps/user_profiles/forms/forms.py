from django import forms

# -------------------------------------------------------------------------------
# Local Imports: Civic User Profile Model
# -------------------------------------------------------------------------------
from apps.user_profiles.models import UserProfile


# ===============================================================================
# DynamicProfileCompletionForm
# - Dynamically renders only the missing profile fields required for civic use.
# ===============================================================================

class DynamicProfileCompletionForm(forms.ModelForm):
    """
    A dynamic form that renders only the missing required fields
    from the UserProfile for civic participation.
    """

    # ---------------------------------------------------------------------------
    # Constructor: Filter out already-completed fields based on the profile
    # ---------------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        user_profile = kwargs.pop('user_profile', None)
        super().__init__(*args, **kwargs)

        if user_profile:
            # Loop over a static copy of field names (because we're modifying the dict)
            for field_name in list(self.fields.keys()):
                value = getattr(user_profile, field_name, None)

                # For ManyToMany fields (e.g., civic_interest_areas), use .exists()
                if hasattr(value, 'exists'):
                    if value.exists():
                        self.fields.pop(field_name)

                # For scalar values: remove if they are truthy (i.e., filled)
                elif value not in [None, '', False]:
                    self.fields.pop(field_name)

    # ---------------------------------------------------------------------------
    # Meta Configuration: Defines which fields are relevant for civic completeness
    # ---------------------------------------------------------------------------
    class Meta:
        model = UserProfile
        fields = [
            'age_range',
            'gender',
            'education_level',
            'residency_type',
            'referral_source',
            'county',
            'constituency',
            'ward',
            'county_of_origin',
            'current_country_of_residence',
            'civic_interest_areas',
            'has_voted_before',
            'knows_voting_process',
        ]
