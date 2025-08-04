# apps/user_profiles/urls_htmx.py

from django.urls import path
from apps.user_profiles.views.htmx_whatsapp_field import render_whatsapp_field



urlpatterns = [
    path("htmx/whatsapp-field/", render_whatsapp_field, name="htmx_whatsapp_field"),
]
