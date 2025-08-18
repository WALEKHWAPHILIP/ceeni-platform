# apps/ceeni_captcha/models/jumbled_leaders.py

from django.db import models
from .captcha_base import CaptchaBase

class JumbledLeaderCaptcha(CaptchaBase):
    """
    Captcha where the user must rearrange letters of a known Kenyan leader.
    Example: 'IMO' → 'MOI'
    """
    class Meta:
        verbose_name = "Jumbled Leader Captcha"
        verbose_name_plural = "Jumbled Leader Captchas"
