# apps/user_profiles/urls.py

from django.urls import path, include

# ===============================
# Import View Handlers for Each Step
# ===============================
from .views.screen_1_basic_info_view import screen_1_basic_info
from .views.screen_2_location_view import screen_2_location_info
from .views.screen_3_origin_and_residency import screen_3_origin_and_residency
from .views.screen_4_civic_interests import screen_4_civic_interests
from .views.screen_5_communication_view import screen_5_communication
from .views.screen_6_referral_source_view import screen_6_referral_source
from .views.screen_7_confirmation_and_save_view import screen_7_confirmation_and_save
from .views.profile_resume_prompt import resume_or_logout

# Utility and AJAX-related views
from .views.htmx_autocomplete import htmx_load_constituencies, htmx_load_wards
from .views.profile_checker import profile_checker

# ===============================
# Namespace for Reverse URL Resolution
# ===============================
app_name = "user_profiles"

# ===============================
# URL Patterns for Profile Wizard & Dynamic Views
# ===============================
urlpatterns = [

    # ------------------------------
    # Profile Registration Wizard Steps
    # ------------------------------
    path('basic-info/', screen_1_basic_info, name='screen_1'),                # Step 1: Age, Gender, Education
    path('location/', screen_2_location_info, name='screen_2'),               # Step 2: County → Constituency → Ward
    path('origin-residency/', screen_3_origin_and_residency, name='screen_3'),# Step 3: Place of Origin and Current Residence
    path('civic-interests/', screen_4_civic_interests, name='screen_4'),      # Step 4: Civic Interests
    path('communication/', screen_5_communication, name='screen_5'),          # Step 5: Notification Preference + WhatsApp
    path('referral-source/', screen_6_referral_source, name='screen_6'),      # Step 6: How user heard about CEENI
    path('confirm-save/', screen_7_confirmation_and_save, name='screen_7'),   # Step 7: Final Review & Save

    # ------------------------------
    # HTMX Endpoints for Dynamic Dropdowns
    # ------------------------------
    path('htmx/constituencies/', htmx_load_constituencies, name='htmx_constituencies'),
    path('htmx/wards/', htmx_load_wards, name='htmx_wards'),

    # ------------------------------
    # Profile Completion Enforcer
    # Redirects incomplete user profiles back to the wizard
    # ------------------------------
    path("resume/", resume_or_logout, name="resume_prompt"),

    # ------------------------------
    # Profile Completion Checker
    # Redirects completed users away from wizard
    # ------------------------------
    path('check-profile/', profile_checker, name='profile_checker'),

    # ------------------------------
    # HTMX Partials (e.g., Conditional WhatsApp Field)
    # Included separately to resolve `{% url 'user_profiles:htmx_whatsapp_field' %}`
    # ------------------------------
    path('', include('apps.user_profiles.urls_htmx')),
]





