"""
FILE: apps/ceeni_captcha/management/commands/import_jumbled_ward_captcha.py

PURPOSE:
    Concrete management command to import jumbled ward captcha data from
    `jumbled_ward_captcha.csv` into the JumbledWardCaptcha model.
    This leverages the generic base command `BaseImportCaptchaCommand`.

CSV REQUIRED (relative to your project root):
    data/csv/captcha/jumbled_ward_captcha.csv

CSV STRUCTURE:
    question_text,correct_answer,hint,explanation,difficulty,tags,active

USAGE:
    python manage.py import_jumbled_ward_captcha

NOTES:
    - Idempotent: rows are matched by a slug derived from the first 80 chars of `question_text`.
      Existing rows are updated; new ones are created.
    - Booleans in CSV’s 'active' column should be TRUE/FALSE (case-insensitive).
"""

# Import the base class that implements the CSV parsing + upsert logic
from .base_import_captcha import BaseImportCaptchaCommand

# Import the concrete model that stores these captchas
from apps.ceeni_captcha.models import JumbledWardCaptcha


class Command(BaseImportCaptchaCommand):
    """
    Importer for JumbledWardCaptcha:
    - Points to the proper model
    - Points to the correct CSV filename
    """
    # Help text shown in `python manage.py help import_jumbled_ward_captcha`
    help = "Imports jumbled ward captcha questions into the JumbledWardCaptcha model."

    # Concrete Django model to import into
    model = JumbledWardCaptcha

    # CSV file name (under data/csv/captcha/)
    file_name = "jumbled_ward_captcha.csv"
