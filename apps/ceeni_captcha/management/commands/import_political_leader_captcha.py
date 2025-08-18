"""
FILE: apps/ceeni_captcha/management/commands/import_political_leader_captcha.py

PURPOSE:
    Concrete management command to import political leader captcha data from
    `political_party_leaders.csv` into the PoliticalPartyLeaderCaptcha model.
    This file leverages the generic base command `BaseImportCaptchaCommand`.

    PoliticalPartyLeaderCaptcha includes questions about leadership history
    and party affiliations within Kenya's political landscape.

REQUIRED CSV FILE:
    data/csv/captcha/political_party_leaders.csv

CSV STRUCTURE:
    question_text,correct_answer,hint,explanation,difficulty,tags,active

USAGE:
    python manage.py import_political_leader_captcha
"""

# Import base class containing CSV import logic
from .base_import_captcha import BaseImportCaptchaCommand

# Import specific Django model for PoliticalPartyLeaderCaptcha
from apps.ceeni_captcha.models import PoliticalPartyLeaderCaptcha


class Command(BaseImportCaptchaCommand):
    """
    Command class inheriting from BaseImportCaptchaCommand.
    Specifies the concrete model and CSV filename to import.
    """
    help = "Imports political leader captcha questions into the PoliticalPartyLeaderCaptcha model."

    model = PoliticalPartyLeaderCaptcha
    file_name = "political_party_leaders.csv"
