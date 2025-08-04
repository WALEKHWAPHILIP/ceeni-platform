from django.urls import path
from .views import (
    index_view,
    why_this_bill_matters_view,
)

# ───────────────────────────────────────────────────────────────────────────────
# FILE: apps/landing/urls.py
# PURPOSE:
#   - Routes public-facing URLs (homepage, about, contact) to corresponding views.
#   - Acts as the entry point for CEENI’s civic engagement and motivational content.
# ───────────────────────────────────────────────────────────────────────────────

app_name = "landing"  # Namespacing for reverse URL resolution (e.g., 'landing:index')

urlpatterns = [
    # Homepage
    path('', index_view, name='index'),

    # Narratives page
    path("why-this-bill-matters/", why_this_bill_matters_view, name="why_this_bill_matters"),

    # Example future routes (uncomment or add as needed)
    # path('about/', views.about, name='about'),
    # path('contact/', views.contact, name='contact'),
]
