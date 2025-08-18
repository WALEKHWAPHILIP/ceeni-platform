# apps/ceeni_captcha/views/htmx/captcha_reload.py

from django.shortcuts import render
from apps.ceeni_captcha.forms.captcha_mixin import CaptchaFieldMixin


def reload_captcha_partial_view(request):
    """
    HTMX view to reload a new captcha partial block.
    
    This regenerates a new question from the pool of active captcha models,
    respecting difficulty range and session state. Only the fieldset is returned,
    not the entire form.
    """
    form = CaptchaFieldMixin(request=request)

    return render(
        request,
        "common/forms/partials/_captcha_block.html",
        {
            "form": form,
            "captcha_model_label": getattr(form, "_current_captcha", None).get_model_label() if hasattr(form, "_current_captcha") else None
        }
    )


