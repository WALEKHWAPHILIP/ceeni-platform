from django.urls import path
from . import views

# ───────────────────────────────────────────────────────────────────────────────
# FILE: apps/user_accounts/urls.py
# PURPOSE:
#   - Routes all URLs related to user authentication and account management.
#   - Includes login, logout, registration, password reset, and profile settings.
# ───────────────────────────────────────────────────────────────────────────────

app_name = "user_accounts"  # Enables namespaced URL resolution (e.g., 'user_accounts:login')

urlpatterns = [
    # ------------------------------------------------------------------------------
    # User Login Route
    # ------------------------------------------------------------------------------
    # Renders login form and handles authentication
    path('login/', views.CustomLoginView.as_view(), name='login'),

    # ------------------------------------------------------------------------------
    # User Logout Route
    # ------------------------------------------------------------------------------
    # Logs out the user and redirects to the root or login page
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),

    # ------------------------------------------------------------------------------
    # User Registration Route
    # ------------------------------------------------------------------------------
    # Handles user sign-up and form validation
    path('register/', views.register, name='register'),

    # Future routes (uncomment to activate)
    # path('reset-password/', views.reset_password, name='reset_password'),
    # path('profile/', views.profile_view, name='profile'),
]
