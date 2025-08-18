"""
FILE: apps/ceeni_captcha/management/commands/import_jumbled_leader_captcha.py

PURPOSE:
    Import jumbled leader captcha data from `jumbled_leader_captcha.csv`
    into the JumbledLeaderCaptcha model. This reuses the generic importer
    in `BaseImportCaptchaCommand`.

REQUIRED CSV (relative to project root):
    data/csv/captcha/jumbled_leader_captcha.csv

CSV COLUMNS:
    question_text,correct_answer,hint,explanation,difficulty,tags,active

USAGE:
    python manage.py import_jumbled_leader_captcha

NOTES:
    - Idempotent: rows are keyed by a slugified prefix of `question_text` (first 80 chars).
      If the slug exists, the row is updated; otherwise it’s created.
    - Booleans: the 'active' column should be TRUE/FALSE (case-insensitive).
"""

# Import the base class that implements CSV parsing + upsert behavior
from .base_import_captcha import BaseImportCaptchaCommand

# Import the concrete model that stores these captchas
from apps.ceeni_captcha.models import JumbledLeaderCaptcha


class Command(BaseImportCaptchaCommand):
    """
    Concrete management command for importing JumbledLeaderCaptcha rows
    from `data/csv/captcha/jumbled_leader_captcha.csv`.
    """
    help = "Imports jumbled leader captcha questions into the JumbledLeaderCaptcha model."

    # Target Django model
    model = JumbledLeaderCaptcha

    # CSV filename under data/csv/captcha/
    file_name = "jumbled_leader_captcha.csv"
