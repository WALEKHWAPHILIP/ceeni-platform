"""
FILE: apps/ceeni_captcha/management/commands/import_jumbled_county_captcha.py

PURPOSE:
    Concrete management command to import jumbled county captcha data from
    `jumbled_county_captcha.csv` into the JumbledCountyCaptcha model.
    This file leverages the generic base command `BaseImportCaptchaCommand`.

    JumbledCountyCaptcha includes jumbled-letter challenges where the player
    unscrambles the county name based on the given hint.

REQUIRED CSV FILE:
    data/csv/captcha/jumbled_county_captcha.csv

CSV STRUCTURE:
    question_text,correct_answer,hint,explanation,difficulty,tags,active

USAGE:
    python manage.py import_jumbled_county_captcha
"""

# Import base class containing CSV import logic
from .base_import_captcha import BaseImportCaptchaCommand

# Import specific Django model for JumbledCountyCaptcha
from apps.ceeni_captcha.models import JumbledCountyCaptcha


class Command(BaseImportCaptchaCommand):
    """
    Command class inheriting from BaseImportCaptchaCommand.
    Specifies the concrete model and CSV filename to import.
    """
    help = "Imports jumbled county captcha questions into the JumbledCountyCaptcha model."

    model = JumbledCountyCaptcha
    file_name = "jumbled_county_captcha.csv"
