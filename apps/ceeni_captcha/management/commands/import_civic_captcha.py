"""
FILE: apps/ceeni_captcha/management/commands/import_civic_captcha.py

PURPOSE:
    Concrete management command to import civic captcha data from
    `civic_captcha.csv` into the CivicCaptcha model. This file leverages the
    generic base command `BaseImportCaptchaCommand`.

    CivicCaptcha includes civic education trivia-style questions about
    Kenya's governance, constitution, geography, history, and culture.

REQUIRED CSV FILE:
    data/csv/captcha/civic_captcha.csv

CSV STRUCTURE:
    question_text,correct_answer,hint,explanation,difficulty,tags,active

USAGE:
    python manage.py import_civic_captcha
"""

# Import base class containing CSV import logic
from .base_import_captcha import BaseImportCaptchaCommand

# Import specific Django model for CivicCaptcha
from apps.ceeni_captcha.models import CivicCaptcha

class Command(BaseImportCaptchaCommand):
    """
    Command class inheriting from BaseImportCaptchaCommand.
    Specifies the concrete model and CSV filename to import.
    """
    # Help message shown when running `python manage.py help`
    help = "Imports civic captcha questions into the CivicCaptcha model."

    # Concrete Django model to import data into
    model = CivicCaptcha

    # Filename of the CSV file relative to data/csv/captcha/
    file_name = "civic_captcha.csv"
