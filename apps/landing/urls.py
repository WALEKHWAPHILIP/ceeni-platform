from django.urls import path
from . import views

# ───────────────────────────────────────────────────────────────
# App Name:
#   Used for namespacing URL names when this app's URLs
#   are included in the project’s main `urls.py`.
#   Example usage: {% url 'landing:read_bill' %}
# ───────────────────────────────────────────────────────────────
app_name = "landing"

# ───────────────────────────────────────────────────────────────
# URL Patterns for Public-Facing CEENI Civic Pages
# ───────────────────────────────────────────────────────────────
urlpatterns = [

    # Home Page (Index)
    path('', views.index_view, name='index'),

    # Narrative Explainer: "Why This Bill Matters"
    path('why-this-bill-matters/', views.why_this_bill_matters_view, name='why_this_bill_matters'),

    # EEPR Bill (Full Legal Text)
    path('read-the-bill/', views.read_the_bill_view, name='read_bill'),

    # Friendly Guide (English)
    path('friendly-guide-en/', views.friendly_guide_en_view, name='friendly_guide_en'),

    # Friendly Guide (Swahili)
    path('friendly-guide-sw/', views.friendly_guide_sw_view, name='friendly_guide_sw'),

    # Historical Background and Policy Rationale
    path('historical-background/', views.bill_history_view, name='bill_history'),

    # Constitution of Kenya (2010) – Summary and PDF Reference
    path('2010-constitution/', views.constitution_2010_view, name='constitution_2010'),

    # Civic Documents List – All CEENI Resources in One Page
    path('ceeni-documents/', views.docs_list_view, name='docs_list'),
]
