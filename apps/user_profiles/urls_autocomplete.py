# ───────────────────────────────────────────────────────────────────────────────
# FILE: apps/user_profiles/urls_autocomplete.py
# PURPOSE:
#     - Defines URL routes for AJAX-powered Select2 autocompletes.
#     - Linked to views using Django Autocomplete Light (DAL).
# USAGE:
#     - Included in the main user_profiles/urls.py with `include()`.
#     - Supports dynamic dropdowns filtered by county or constituency.
# ───────────────────────────────────────────────────────────────────────────────

from django.urls import path
from .views.autocomplete import ConstituencyAutocomplete, WardAutocomplete

urlpatterns = [
    path(
        "constituency-autocomplete/",
        ConstituencyAutocomplete.as_view(),
        name="constituency-autocomplete"
    ),
    path(
        "ward-autocomplete/",
        WardAutocomplete.as_view(),
        name="ward-autocomplete"
    ),
]
