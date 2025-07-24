# ──────────────────────────────────────────────────────────────────────────
# FILE: apps/user_profiles/views/screen_4_civic_interests.py
# PURPOSE: Handles screen 4 of CEENI registration – Civic Interests
# ──────────────────────────────────────────────────────────────────────────

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.user_profiles.forms.screen_4_civic_interests import Screen4CivicInterestsForm


@login_required
def screen_4_civic_interests(request):
    """
    Renders and processes Step 4 – Civic Interests form.
    """
    profile = request.user.userprofile

    if request.method == "POST":
        form = Screen4CivicInterestsForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("user_profiles:screen_5")  # Placeholder
    else:
        form = Screen4CivicInterestsForm(instance=profile)

    return render(request, "user_profiles/screens/s4_civic_interests.html", {
        "form": form,
        "completion": profile.completion_percentage(),
    })
