# apps/user_profiles/views/screen_7_confirmation_and_save_view.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from apps.user_profiles.constants import TOTAL_WIZARD_STEPS
from apps.user_profiles.utils.progress import compute_weighted_completion
from apps.user_profiles.forms.screen_7_confirmation_and_save import Screen7ConfirmationAndSaveForm


@login_required
def screen_7_confirmation_and_save(request):
    """
    Step 7 (Final Confirmation) of the CEENI profile wizard.
    Displays a summary. On submit, triggers save to ensure final state.
    """

    profile = request.user.userprofile

    # 🚫 Prevent early access unless explicitly forced
    if not request.GET.get("force") and profile.get_next_incomplete_screen() != 'user_profiles:screen_7':
        return redirect(profile.get_next_incomplete_screen())

    # Progress tracker (final step)
    step_number = 7
    completion = compute_weighted_completion(step_number)

    if request.method == "POST":
        form = Screen7ConfirmationAndSaveForm(request.POST, instance=profile)
        if form.is_valid():
            # Trigger profile.save() to finalize completion_percentage
            profile.save()
            return redirect("dashboard:home")
    else:
        form = Screen7ConfirmationAndSaveForm(instance=profile)

    return render(
        request,
        "user_profiles/screens/s7_confirmation_and_save.html",
        {
            "form": form,
            "profile": profile,
            "step_number": step_number,
            "total_steps": TOTAL_WIZARD_STEPS,
            "completion": completion,
        },
    )
