# ============================================================================
# FILE: apps/user_profiles/views/profile_checker.py
# PURPOSE:
#     - Enforces profile completeness before user can access civic features.
#     - Dynamically shows only incomplete fields.
#     - Displays percentage completed with motivation.
# ============================================================================

from django.shortcuts import render, redirect
from apps.user_profiles.forms.forms import DynamicProfileCompletionForm


def profile_checker(request):
    """
    Renders a form that allows users to complete their mandatory profile fields.
    Redirects to dashboard if already complete.
    """
    profile = request.user.userprofile
    completion = profile.completion_percentage()

    # If already eligible, skip this screen
    if profile.has_required_profile_fields():
        return redirect("dashboard")  # Replace with your actual dashboard route name

    if request.method == "POST":
        form = DynamicProfileCompletionForm(
            request.POST,
            request.FILES,
            instance=profile,
            user_profile=profile
        )
        if form.is_valid():
            form.save()
            # Re-check after saving
            if profile.has_required_profile_fields():
                return redirect("dashboard")
            return redirect("user_profiles:profile_checker")
    else:
        form = DynamicProfileCompletionForm(instance=profile, user_profile=profile)

    return render(request, "user_profiles/profile_checker.html", {
        "form": form,
        "completion": completion,
    })
