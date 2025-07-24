from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from apps.user_profiles.forms.screen_5_communication import Screen5CommunicationForm


@login_required
def screen_5_communication(request):
    """
    Renders and processes Screen 5 – Communication Preferences (no photo).
    """
    profile = request.user.userprofile

    if request.method == "POST":
        form = Screen5CommunicationForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("user_profiles:screen_6_summary")  # Replace with your actual next screen
    else:
        form = Screen5CommunicationForm(instance=profile)

    return render(request, "user_profiles/screens/s5_communication.html", {
        "form": form,
    })
