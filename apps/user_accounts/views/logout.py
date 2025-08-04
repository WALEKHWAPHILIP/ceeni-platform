"""
apps/user_accounts/views/logout.py

Custom logout view extending Django’s LogoutView.
Simply redirects to the site root or login.
"""

from django.contrib.auth.views import LogoutView


class CustomLogoutView(LogoutView):
    """
    Logs the user out and redirects to the homepage.
    """
    next_page = "/"
