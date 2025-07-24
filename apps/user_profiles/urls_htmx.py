from django.urls import path
from apps.user_profiles.views.htmx_whatsapp_field import render_whatsapp_field

app_name = "user_profiles_htmx"

urlpatterns = [
    path("whatsapp-optin/", render_whatsapp_field, name="whatsapp_optin_partial"),
]
