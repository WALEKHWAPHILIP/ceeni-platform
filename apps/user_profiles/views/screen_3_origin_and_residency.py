# apps/user_profiles/views/screen_3_origin_and_residency.py

"""
Handles Screen 3 (Origin & Residency) of the progressive CEENI registration wizard.
Renders and processes the Origin & Residency form, then redirects to Screen 4 on success.
"""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from apps.user_profiles.constants import TOTAL_WIZARD_STEPS
from apps.user_profiles.utils.progress import compute_weighted_completion
from apps.user_profiles.forms.screen_3_origin_residency import Screen3OriginResidencyForm


@login_required
def screen_3_origin_and_residency(request):
    """
    Step 3 of the profile wizard: Origin & Residency.
    Blocks users from skipping ahead unless explicitly overridden via ?force=true.
    """
    profile = request.user.userprofile

    # 🔐 Enforce screen order unless user forced backward visit (e.g. via "Back" button)
    if not request.GET.get("force") and profile.get_next_incomplete_screen() != 'user_profiles:screen_3':
        return redirect(profile.get_next_incomplete_screen())

    # Setup form and progress context
    step_number = 3
    completion = compute_weighted_completion(step_number)

    if request.method == "POST":
        form = Screen3OriginResidencyForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("user_profiles:screen_4")
    else:
        form = Screen3OriginResidencyForm(instance=profile)

    return render(
        request,
        "user_profiles/screens/s3_origin_and_residency.html",
        {
            "form": form,
            "step_number": step_number,
            "total_steps": TOTAL_WIZARD_STEPS,
            "completion": completion,
        },
    )
