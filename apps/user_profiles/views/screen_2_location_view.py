from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from apps.user_profiles.constants import TOTAL_WIZARD_STEPS
from apps.user_profiles.utils.progress import compute_weighted_completion
from apps.user_profiles.forms.screen_2_location import Screen2LocationForm


@login_required
def screen_2_location_info(request):
    """
    Step 2 of the 7-step profile wizard: Location info.
    Redirects forward if the user's current step is beyond screen 2,
    unless the user explicitly requests to return via ?force=true.
    """
    profile = request.user.userprofile

    # 🚧 Block backward access unless ?force=true
    if not request.GET.get("force") and profile.get_next_incomplete_screen() != 'user_profiles:screen_2':
        return redirect(profile.get_next_incomplete_screen())

    step_number = 2
    completion = compute_weighted_completion(step_number)

    if request.method == "POST":
        form = Screen2LocationForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("user_profiles:screen_3")
    else:
        form = Screen2LocationForm(instance=profile)

    return render(
        request,
        "user_profiles/screens/s2_location_info.html",
        {
            "form": form,
            "step_number": step_number,
            "total_steps": TOTAL_WIZARD_STEPS,
            "completion": completion,
        }
    )
