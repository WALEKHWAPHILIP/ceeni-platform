# apps/ceeni_captcha/models/jumbled_wards.py

from django.db import models
from .captcha_base import CaptchaBase

class JumbledWardCaptcha(CaptchaBase):
    """
    Captcha requiring the user to unscramble the name of a Kenyan electoral ward.
    Example: 'MOONAKI' → 'KIMONANI'
    """
    class Meta:
        verbose_name = "Jumbled Ward Captcha"
        verbose_name_plural = "Jumbled Ward Captchas"
