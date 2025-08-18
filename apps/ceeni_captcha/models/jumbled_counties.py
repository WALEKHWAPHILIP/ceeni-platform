# apps/ceeni_captcha/models/jumbled_counties.py

from django.db import models
from .captcha_base import CaptchaBase

class JumbledCountyCaptcha(CaptchaBase):
    """
    Captcha that challenges the user to reorder letters of Kenyan counties.
    Example: 'AWKEL' → 'LWAEK' → 'KWALE'
    """
    class Meta:
        verbose_name = "Jumbled County Captcha"
        verbose_name_plural = "Jumbled County Captchas"
