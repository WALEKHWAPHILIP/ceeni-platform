# ────────────────────────────────────────────────────────────────
# FILE: apps/user_profiles/views/htmx_autocomplete.py
# PURPOSE: HTMX-based dynamic filters for public registration flow
# ────────────────────────────────────────────────────────────────

from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.user_profiles.models import Constituency, Ward


@login_required
def htmx_load_constituencies(request):
    """
    HTMX view: Returns <option> list of constituencies for a given county_id.
    """
    county_id = request.GET.get("county_id")
    if not county_id:
        return HttpResponseBadRequest("Missing county_id")

    constituencies = Constituency.objects.filter(county_id=county_id).order_by("name")
    return render(request, "user_profiles/partials/_constituency_options.html", {
        "constituencies": constituencies
    })


@login_required
def htmx_load_wards(request):
    """
    HTMX view: Returns <option> list of wards for a given constituency_id.
    """
    constituency_id = request.GET.get("constituency_id")
    if not constituency_id:
        return HttpResponseBadRequest("Missing constituency_id")

    wards = Ward.objects.filter(constituency_id=constituency_id).order_by("name")
    return render(request, "user_profiles/partials/_ward_options.html", {
        "wards": wards
    })
