from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from apps.user_profiles.constants import TOTAL_WIZARD_STEPS
from apps.user_profiles.utils.progress import compute_weighted_completion
from apps.user_profiles.forms.screen_1_basic_info import Screen1BasicInfoForm


@login_required
def screen_1_basic_info(request):
    """
    Step 1 of the 7-step profile wizard.
    If the user's next incomplete screen is NOT screen 1, redirect them to the correct step.
    """
    profile = request.user.userprofile

    # 👁️ Redirect user forward if they already filled this screen
    if profile.get_next_incomplete_screen() != 'user_profiles:screen_1':
        return redirect(profile.get_next_incomplete_screen())

    # Display or process this screen normally
    step_number = 1
    completion = compute_weighted_completion(step_number)

    if request.method == "POST":
        form = Screen1BasicInfoForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("user_profiles:screen_2")
    else:
        form = Screen1BasicInfoForm(instance=profile)

    return render(
        request,
        "user_profiles/screens/s1_basic_info.html",
        {
            "form": form,
            "step_number": step_number,
            "total_steps": TOTAL_WIZARD_STEPS,
            "completion": completion,
        }
    )
