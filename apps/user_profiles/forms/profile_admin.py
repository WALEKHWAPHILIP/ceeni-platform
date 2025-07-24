# ───────────────────────────────────────────────────────────────────────────────
# FILE: apps/user_profiles/forms/profile_admin.py
# PURPOSE:
#     - Custom admin form for UserProfile model.
#     - Integrates Django Autocomplete Light (DAL) with Select2 widgets.
#     - Enables dynamic filtering of location fields (e.g., Ward by Constituency).
# USAGE:
#     - Used in admin registration to enhance UX with AJAX-powered dropdowns.
# DEPENDENCIES:
#     - dal, dal_select2
#     - Autocomplete views registered in urls_autocomplete.py
# ───────────────────────────────────────────────────────────────────────────────

from dal import autocomplete
from django import forms
from apps.user_profiles.models import UserProfile


class UserProfileAdminForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = "__all__"

        widgets = {
            "constituency": autocomplete.ModelSelect2(
                url="constituency-autocomplete",
                forward=["county"]
            ),
            "ward": autocomplete.ModelSelect2(
                url="ward-autocomplete",
                forward=["constituency"]
            ),
        }
