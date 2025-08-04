# =============================================================
# apps/user_profiles/views/profile_resume_prompt.py
# =============================================================
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone


@login_required
def resume_or_logout(request):
    """
    Prompt returning user to resume where they left off or logout.
    Only shown if profile is incomplete.
    """
    profile = request.user.userprofile

    # Auto-redirect complete users
    if profile.is_complete():
        return redirect("dashboard:home")

    # Log current return time
    profile.last_wizard_login_at = timezone.now()
    profile.save(update_fields=["last_wizard_login_at"])

    # Handle decision
    if request.method == "POST":
        if "continue" in request.POST:
            return redirect(profile.get_next_incomplete_screen())
        elif "cancel" in request.POST:
            logout(request)
            return redirect("user_accounts:login")  # or your login page

    return render(request, "user_profiles/screens/resume_prompt.html", {
        "user": request.user,
        "profile": profile,
    })
