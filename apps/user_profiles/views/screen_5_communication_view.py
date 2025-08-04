# apps/user_profiles/views/screen_5_communication_view.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from apps.user_profiles.constants import TOTAL_WIZARD_STEPS
from apps.user_profiles.utils.progress import compute_weighted_completion
from apps.user_profiles.forms.screen_5_communication import Screen5CommunicationForm


@login_required
def screen_5_communication(request):
    """
    Step 5 of the profile wizard: Communication preferences & profile photo.
    Redirects forward only if this is the correct next step, unless ?force=true.
    """
    profile = request.user.userprofile

    # 🔐 Enforce correct screen access unless explicitly forced
    if not request.GET.get("force") and profile.get_next_incomplete_screen() != 'user_profiles:screen_5':
        return redirect(profile.get_next_incomplete_screen())

    # Wizard progress UI
    step_number = 5
    completion = compute_weighted_completion(step_number)

    if request.method == "POST":
        form = Screen5CommunicationForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("user_profiles:screen_6")
    else:
        form = Screen5CommunicationForm(instance=profile)

    return render(
        request,
        "user_profiles/screens/s5_communication.html",
        {
            "form": form,
            "step_number": step_number,
            "total_steps": TOTAL_WIZARD_STEPS,
            "completion": completion,
        },
    )
