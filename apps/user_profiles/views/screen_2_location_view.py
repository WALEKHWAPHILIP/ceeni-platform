# ──────────────────────────────────────────────────────────────────────────
# FILE: apps/user_profiles/views/screen_2_location_view.py
# PURPOSE: Handles screen 2 of CEENI registration – Location Info
# ──────────────────────────────────────────────────────────────────────────

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.user_profiles.forms.screen_2_location import Screen2LocationForm


@login_required
def screen_2_location_info(request):
    """
    Renders and processes Screen 2: County → Constituency → Ward
    """

    profile = request.user.userprofile

    if request.method == "POST":
        form = Screen2LocationForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("user_profiles:screen_3_origin_residency")  # placeholder
    else:
        form = Screen2LocationForm(instance=profile)

    return render(request, "user_profiles/screens/s2_location_info.html", {
        "form": form,
        "completion": profile.completion_percentage(),
    })
