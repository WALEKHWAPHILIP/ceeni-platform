# apps/user_profiles/views/htmx_whatsapp_field.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.user_profiles.forms.screen_5_communication import Screen5CommunicationForm


@login_required
def render_whatsapp_field(request):
    """
    HTMX partial to conditionally render WhatsApp number field
    ONLY if wants_bill_notifications is explicitly True.
    """
    profile = request.user.userprofile
    form = Screen5CommunicationForm(request.POST or None, instance=profile)

    raw_value = request.POST.get("wants_bill_notifications")

    # Normalize True detection (should match form coerce logic)
    wants_notifications = raw_value in ["True", "true", "1", 1, True]

    if wants_notifications:
        return render(request, "user_profiles/partials/_whatsapp_opt_in_field.html", {"form": form})
    else:
        return render(request, "user_profiles/partials/_empty_whatsapp.html", {"form": form})
