# apps/user_profiles/views/screen_6_referral_source_view.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from apps.user_profiles.constants import TOTAL_WIZARD_STEPS
from apps.user_profiles.utils.progress import compute_weighted_completion
from apps.user_profiles.forms.screen_6_referral_source import Screen6ReferralSourceForm


@login_required
def screen_6_referral_source(request):
    """
    Step 6 of the profile wizard: Referral Source.
    Enforces correct progression unless ?force=true is present.
    """
    profile = request.user.userprofile

    # 🔐 Guard to prevent jumping ahead in the wizard
    if not request.GET.get("force") and profile.get_next_incomplete_screen() != 'user_profiles:screen_6':
        return redirect(profile.get_next_incomplete_screen())

    # Progress bar and wizard visuals
    step_number = 6
    completion = compute_weighted_completion(step_number)

    if request.method == "POST":
        form = Screen6ReferralSourceForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("user_profiles:screen_7")
    else:
        form = Screen6ReferralSourceForm(instance=profile)

    return render(
        request,
        "user_profiles/screens/s6_referral_source.html",
        {
            "form": form,
            "step_number": step_number,
            "total_steps": TOTAL_WIZARD_STEPS,
            "completion": completion,
        },
    )
