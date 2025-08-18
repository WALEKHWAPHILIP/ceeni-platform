"""
FILE: apps/ceeni_captcha/management/commands/base_import_captcha.py

PURPOSE:
    This is an abstract base management command for importing captcha questions
    into the CEENI platform from standardized CSV files. This command provides
    the core logic for parsing CSV data and inserting or updating records in
    corresponding Django models derived from CaptchaBase.

USAGE:
    Subclasses must define:
        - model: Concrete Django captcha model (e.g., CivicCaptcha, JumbledCountyCaptcha)
        - file_name: CSV file name containing captcha questions located at data/csv/captcha/

EXAMPLE SUBCLASSES:
    - import_civic_captcha.py
    - import_jumbled_county_captcha.py
    - import_jumbled_constituency_captcha.py
    - import_jumbled_leader_captcha.py
    - import_jumbled_ward_captcha.py

CSV FILE STRUCTURE (common for all captcha CSVs):
    question_text,correct_answer,hint,explanation,difficulty,tags,active

DEPENDENCIES:
    - CSV_DATA_DIR: Defined in config/settings/base.py, points to the data/csv directory.

"""

import csv
from django.core.management.base import BaseCommand, CommandError
from django.utils.text import slugify
from config.settings.base import CSV_DATA_DIR


class BaseImportCaptchaCommand(BaseCommand):
    help = "Imports captcha data from a CSV file into the specified model."

    # Concrete captcha model to import data into (e.g., CivicCaptcha)
    model = None

    # Filename for the CSV data file (relative to data/csv/captcha/)
    file_name = None

    def handle(self, *args, **options):
        # Ensure subclass correctly defines 'model'
        if not self.model:
            raise CommandError("The 'model' attribute must be set in the subclass.")

        # Ensure subclass correctly defines 'file_name'
        if not self.file_name:
            raise CommandError("The 'file_name' attribute must be set in the subclass.")

        # Construct full CSV file path
        file_path = CSV_DATA_DIR / "captcha" / self.file_name

        created_count = 0
        updated_count = 0

        # Attempt to read and import CSV data
        try:
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    # Generate a unique slug based on question_text
                    slug = slugify(row['question_text'][:80])

                    # Default values extracted from CSV columns
                    defaults = {
                        'correct_answer': row['correct_answer'].strip(),
                        'hint': row['hint'].strip(),
                        'explanation': row['explanation'].strip(),
                        'difficulty': int(row['difficulty']),
                        'tags': row['tags'].strip(),
                        'active': row['active'].strip().lower() == 'true'
                    }

                    # Create or update captcha record
                    obj, created = self.model.objects.update_or_create(
                        slug=slug,
                        defaults={**defaults, 'question_text': row['question_text']}
                    )

                    # Increment counters based on created or updated status
                    if created:
                        created_count += 1
                    else:
                        updated_count += 1

            # Success message after completing import
            self.stdout.write(
                self.style.SUCCESS(
                    f"Import completed: {created_count} created, {updated_count} updated."
                )
            )

        # Error handling for missing CSV file
        except FileNotFoundError:
            raise CommandError(f"CSV file not found: {file_path}")

        # General exception handling for debugging and stability
        except Exception as e:
            raise CommandError(f"An unexpected error occurred: {e}")
