from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.user_profiles.forms.screen_5_communication import Screen5CommunicationForm

@login_required
def render_whatsapp_field(request):
    """
    HTMX partial to render WhatsApp number field if notifications are opted in.
    """
    profile = request.user.userprofile
    form = Screen5CommunicationForm(instance=profile)
    return render(request, "user_profiles/partials/_whatsapp_opt_in_field.html", {"form": form})
