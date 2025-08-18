# apps/ceeni_captcha/models/jumbled_constituencies.py

from django.db import models
from .captcha_base import CaptchaBase

class JumbledConstituencyCaptcha(CaptchaBase):
    """
    Captcha where users unscramble Kenyan constituency names.
    Example: 'DORGNARAG' → 'GARDNAROG' → 'GARISSA NORTH'
    """
    class Meta:
        verbose_name = "Jumbled Constituency Captcha"
        verbose_name_plural = "Jumbled Constituency Captchas"
