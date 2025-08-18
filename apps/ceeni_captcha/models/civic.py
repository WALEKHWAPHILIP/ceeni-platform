# apps/ceeni_captcha/models/civic.py

from django.db import models
from .captcha_base import CaptchaBase

class CivicCaptcha(CaptchaBase):
    """
    Trivia-style questions about Kenya's civic structure, elections, constitution, etc.
    Example: "How many counties are there in Kenya?"
    """
    class Meta:
        verbose_name = "Civic Captcha"
        verbose_name_plural = "Civic Captchas"
