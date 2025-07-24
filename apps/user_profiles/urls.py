# =======================
# Django Imports
# =======================
from django.urls import path

# =======================
# Local App Views
# =======================
from .views.screen_1_basic_info_view import screen_1_basic_info
from .views.screen_2_location_view import screen_2_location_info
from .views.htmx_autocomplete import htmx_load_constituencies, htmx_load_wards
from .views.screen_3_origin_and_residency import screen_3_origin_and_residency
from .views.screen_4_civic_interests import screen_4_civic_interests
from .views.screen_5_communication_view import screen_5_communication
from .views.screen_6_confirmation_and_save_view import screen_6_confirmation_and_save

from .views.profile_checker import profile_checker

# =======================
# App Namespace
# =======================
app_name = "user_profiles"


# =======================
# URL Patterns
# =======================
urlpatterns = [

    # -----------------------------------------------
    # Step 1: Basic Information (age, gender, education)
    # URL: /profile/basic-info/
    # -----------------------------------------------
    path('basic-info/', screen_1_basic_info, name='screen_1'),

    # -----------------------------------------------
    # Step 2: Location (county ➝ constituency ➝ ward)
    # URL: /profile/location/
    # -----------------------------------------------
    path('location/', screen_2_location_info, name='screen_2'),

    # -----------------------------------------------
    # Step 3: Origin and Residency
    # URL: /profile/origin-residency/
    # -----------------------------------------------
    path('origin-residency/', screen_3_origin_and_residency, name='screen_3'),

    # -----------------------------------------------
    # Step 4: Civic Interests and Participation
    # URL: /profile/civic-interests/
    # -----------------------------------------------
    path('civic-interests/', screen_4_civic_interests, name='screen_4'),

    # -----------------------------------------------
    # Step 5: Communication Preferences & Profile Image
    # URL: /profile/communication-image/
    # -----------------------------------------------
    path('communication-image/', screen_5_communication, name='screen_5'),

    # -----------------------------------------------
    # Step 6: Confirmation and Final Save
    # URL: /profile/confirm-save/
    # -----------------------------------------------
    path('confirm-save/', screen_6_confirmation_and_save, name='screen_6'),

    # -----------------------------------------------
    # HTMX Dynamic Dropdown Loaders
    # These endpoints are called via HTMX (AJAX)
    # to dynamically populate constituency and ward
    # options based on the selected county or constituency.
    # -----------------------------------------------
    path("htmx/constituencies/", htmx_load_constituencies, name="htmx_constituencies"),
    path("htmx/wards/", htmx_load_wards, name="htmx_wards"),

    # -----------------------------------------------
    # Profile Completion Check Endpoint
    # URL: /profile/check-profile/
    # Purpose: Used to verify if a user has completed their profile,
    # often triggered after login before redirecting to dashboard.
    # -----------------------------------------------
    path('check-profile/', profile_checker, name='profile_checker'),

]
