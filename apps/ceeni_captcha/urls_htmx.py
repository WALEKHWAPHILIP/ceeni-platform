# apps/ceeni_captcha/urls_htmx.py

from django.urls import path
from .views.htmx.captcha_reload import reload_captcha_partial_view

app_name = "ceeni_captcha"

urlpatterns = [
    path("captcha/reload/", reload_captcha_partial_view, name="captcha_reload"),
]
