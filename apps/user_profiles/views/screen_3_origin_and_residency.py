# ──────────────────────────────────────────────────────────────────────────
# FILE: apps/user_profiles/views/screen_3_origin_and_residency.py
# PURPOSE: Handles screen 3 of CEENI registration – Origin & Residency
# ──────────────────────────────────────────────────────────────────────────

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.user_profiles.forms.screen_3_origin_residency import Screen3OriginResidencyForm


@login_required
def screen_3_origin_and_residency(request):
    """
    Renders and processes Screen 3: Origin & Residency.
    """

    profile = request.user.userprofile

    if request.method == "POST":
        form = Screen3OriginResidencyForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("user_profiles:screen_4")  # Placeholder for next step
    else:
        form = Screen3OriginResidencyForm(instance=profile)

    return render(request, "user_profiles/screens/s3_origin_and_residency.html", {
        "form": form,
        "completion": profile.completion_percentage(),
    })
