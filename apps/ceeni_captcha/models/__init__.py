# apps/ceeni_captcha/models/__init__.py

"""
This file ensures all concrete captcha models are automatically imported
when the models package is accessed (e.g., during admin registration,
signal connection, testing, or introspection by Django).

By explicitly importing each model here and listing them in __all__,
we allow Django's autodiscovery mechanisms — especially those used in
admin.py, serializers, forms, and migrations — to work seamlessly.

This makes our modular captcha system easier to scale and maintain.
"""

from .civic import CivicCaptcha
from .jumbled_leaders import JumbledLeaderCaptcha
from .jumbled_wards import JumbledWardCaptcha
from .jumbled_constituencies import JumbledConstituencyCaptcha
from .jumbled_counties import JumbledCountyCaptcha
from .political_leaders import PoliticalPartyLeaderCaptcha

__all__ = [
    "CivicCaptcha",
    "JumbledLeaderCaptcha",
    "JumbledWardCaptcha",
    "JumbledConstituencyCaptcha",
    "JumbledCountyCaptcha",
    "PoliticalPartyLeaderCaptcha",
]


