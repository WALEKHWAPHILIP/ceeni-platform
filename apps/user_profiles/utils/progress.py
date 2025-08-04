# apps/user_profiles/utils/progress.py

from typing import List, Type
from django import forms

from apps.user_profiles.forms.screen_1_basic_info import Screen1BasicInfoForm
from apps.user_profiles.forms.screen_2_location import Screen2LocationForm
from apps.user_profiles.forms.screen_3_origin_residency import Screen3OriginResidencyForm
from apps.user_profiles.forms.screen_4_civic_interests import Screen4CivicInterestsForm
from apps.user_profiles.forms.screen_5_communication import Screen5CommunicationForm
from apps.user_profiles.forms.screen_6_referral_source import Screen6ReferralSourceForm
from apps.user_profiles.forms.screen_7_confirmation_and_save import Screen7ConfirmationAndSaveForm

WIZARD_FORMS: List[Type[forms.Form]] = [
    Screen1BasicInfoForm,
    Screen2LocationForm,
    Screen3OriginResidencyForm,
    Screen4CivicInterestsForm,
    Screen5CommunicationForm,
    Screen6ReferralSourceForm,
    Screen7ConfirmationAndSaveForm,
]

def compute_weighted_completion(step_number: int) -> int:
    """
    Calculates a weighted completion percentage based on how many fields
    each screen’s form has. Screens with more inputs count for more of the bar.
    """
    # Count fields on each form
    field_counts = [len(form_class().fields) for form_class in WIZARD_FORMS]
    total_fields = sum(field_counts)

    if total_fields == 0:
        return 0

    # Sum up all fields in completed steps
    # step_number is 1-based
    completed_fields = sum(field_counts[:step_number])

    return int((completed_fields / total_fields) * 100)
