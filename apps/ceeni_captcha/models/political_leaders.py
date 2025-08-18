# apps/ceeni_captcha/models/political_leaders.py

from django.db import models
from .captcha_base import CaptchaBase

class PoliticalPartyLeaderCaptcha(CaptchaBase):
    """
    Captcha with questions about political party leadership in Kenya.
    Based on factual historical or current political party affiliations and leadership.
    """
    class Meta:
        verbose_name = "Political Party Leader Captcha"
        verbose_name_plural = "Political Party Leader Captchas"
