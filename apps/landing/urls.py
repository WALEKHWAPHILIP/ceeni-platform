from django.urls import path
from . import views

# ───────────────────────────────────────────────────────────────────────────────
# FILE: apps/landing/urls.py
# PURPOSE:
#   - Routes public-facing URLs (homepage, about, contact) to corresponding views.
#   - Acts as the entry point for CEENI’s civic engagement and motivational content.
# ───────────────────────────────────────────────────────────────────────────────

app_name = "landing"  # Namespacing for reverse URL resolution (e.g., 'landing:index')

urlpatterns = [
    # ------------------------------------------------------------------------------
    # Homepage Route
    # ------------------------------------------------------------------------------
    # Maps the root URL ('/') to the Landing Page View.
    # This is the CEENI public-facing homepage with motivational civic content.
    path('', views.index, name='index'),
    
    # Example future routes (uncomment or add as needed)
    # path('about/', views.about, name='about'),
    # path('contact/', views.contact, name='contact'),
]
