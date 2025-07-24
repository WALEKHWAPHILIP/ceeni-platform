# ────────────────────────────────────────────────────────────────────────────────
# FILE: apps/user_profiles/views/screen_1_basic_info_view.py
# PURPOSE: Handles screen 1 of the progressive CEENI registration flow.
# ────────────────────────────────────────────────────────────────────────────────

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from apps.user_profiles.forms.screen_1_basic_info import Screen1BasicInfoForm


@login_required
def screen_1_basic_info(request):
    """
    Renders and processes Screen 1 (Basic Info) form.
    """

    profile = request.user.userprofile

    if request.method == "POST":
        form = Screen1BasicInfoForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("user_profiles:screen_2_location")  # Placeholder for next step
    else:
        form = Screen1BasicInfoForm(instance=profile)

    return render(request, "user_profiles/screens/s1_basic_info.html", {
        "form": form,
        "completion": profile.completion_percentage(),
    })
