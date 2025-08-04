# apps/user_profiles/views/screen_4_civic_interests.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from apps.user_profiles.constants import TOTAL_WIZARD_STEPS
from apps.user_profiles.utils.progress import compute_weighted_completion
from apps.user_profiles.forms.screen_4_civic_interests import Screen4CivicInterestsForm


@login_required
def screen_4_civic_interests(request):
    """
    Step 4 of the profile wizard: Civic Interests.
    Prevents unauthorized skipping unless user arrives via a forced back link (?force=true).
    """
    profile = request.user.userprofile

    # 🔐 Guard access unless coming from previous step or with ?force=true
    if not request.GET.get("force") and profile.get_next_incomplete_screen() != 'user_profiles:screen_4':
        return redirect(profile.get_next_incomplete_screen())

    # Wizard UI progress metadata
    step_number = 4
    completion = compute_weighted_completion(step_number)


    if request.method == "POST":
        form = Screen4CivicInterestsForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            # Refresh the profile from the database to ensure M2M fields (like civic_interest_areas)
            # are up-to-date in memory—especially important for logic like get_next_incomplete_screen()
            profile.refresh_from_db()
            return redirect("user_profiles:screen_5")
    else:
        form = Screen4CivicInterestsForm(instance=profile)

    return render(
        request,
        "user_profiles/screens/s4_civic_interests.html",
        {
            "form": form,
            "step_number": step_number,
            "total_steps": TOTAL_WIZARD_STEPS,
            "completion": completion,
        },
    )
