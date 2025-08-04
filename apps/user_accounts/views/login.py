"""
apps/user_accounts/views/login.py

Custom login view extending Django’s built-in LoginView.
Redirects user based on profile completion status.
"""

# =============================================================
# LOGIN VIEW: user_accounts/views/login.py
# =============================================================
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from ..forms.forms_auth import LoginForm


class CustomLoginView(LoginView):
    """
    Handles login flow and post-login redirection.
    If the user has a complete profile, redirect to dashboard.
    Otherwise, redirect to a 'resume-or-exit' confirmation page.
    """
    template_name = "user_accounts/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True  # Prevents logged-in users from accessing the login page again; redirects using get_success_url()


    def get_success_url(self):
        user = self.request.user
        profile = getattr(user, "userprofile", None)

        if profile is None:
            # Defensive fallback — start at screen 1
            return reverse_lazy("user_profiles:screen_1")

        if profile.is_complete():
            return reverse_lazy("dashboard:home")  # Replace with actual dashboard route

        # 🚨 NEW: Redirect to resume prompt, not wizard directly
        return reverse_lazy("user_profiles:resume_prompt")

