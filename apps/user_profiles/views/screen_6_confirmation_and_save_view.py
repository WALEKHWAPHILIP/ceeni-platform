from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


@login_required
def screen_6_confirmation_and_save(request):
    """
    Placeholder view for Screen 6 – Confirmation and Final Save.
    Renders a summary confirmation page (to be implemented in detail).
    """
    user = request.user
    profile = user.userprofile

    if request.method == "POST":
        # Placeholder for save logic (e.g. mark profile complete, trigger notifications, etc.)
        return redirect("dashboard")  # Replace with actual final destination

    return render(request, "user_profiles/screens/s6_confirmation_and_save.html", {
        "user": user,
        "profile": profile,
    })
