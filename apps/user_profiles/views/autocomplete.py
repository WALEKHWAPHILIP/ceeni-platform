# ───────────────────────────────────────────────────────────────────────────────
# FILE: apps/user_profiles/views/autocomplete.py
# PURPOSE:
#     - Provides Select2-powered autocomplete views for user profile forms.
#     - Dynamically filters Constituency and Ward choices based on forwarded fields.
# DEPENDENCIES:
#     - django-autocomplete-light (dal, dal_select2)
#     - user_profiles.models.Constituency, Ward
# ───────────────────────────────────────────────────────────────────────────────

from dal import autocomplete
from django.db.models import Q
from apps.user_profiles.models import Constituency, Ward


class ConstituencyAutocomplete(autocomplete.Select2QuerySetView):
    """
    Autocomplete for constituencies, optionally filtered by selected county.
    """

    def get_queryset(self):
        qs = Constituency.objects.all()

        county_id = self.forwarded.get('county', None)
        if county_id:
            qs = qs.filter(county_id=county_id)

        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs


class WardAutocomplete(autocomplete.Select2QuerySetView):
    """
    Autocomplete for wards, optionally filtered by selected constituency.
    """

    def get_queryset(self):
        qs = Ward.objects.all()

        constituency_id = self.forwarded.get('constituency', None)
        if constituency_id:
            qs = qs.filter(constituency_id=constituency_id)

        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs
