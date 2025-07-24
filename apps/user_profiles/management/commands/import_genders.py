# ------------------------------------------------------------------------------
# Import Gender options from CSV with position, code, label fields.
# If Gender already exists, update label or position if changed.
# ------------------------------------------------------------------------------

import csv
from django.core.management.base import BaseCommand
from django.conf import settings
from apps.user_profiles.models.demographics import Gender


CSV_PATH = settings.CSV_DATA_DIR / "genders.csv"


class Command(BaseCommand):
    help = "Import gender options from data/csv/genders.csv"

    def handle(self, *args, **options):
        if not CSV_PATH.exists():
            self.stderr.write(self.style.ERROR(f"❌ File not found: {CSV_PATH}"))
            return

        created, skipped = 0, 0

        with open(CSV_PATH, newline='', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)

            for idx, row in enumerate(reader, start=1):  # Position starts from 1
                code = row.get("code", "").strip()
                label = row.get("label", "").strip()

                if not code or not label:
                    self.stderr.write(self.style.WARNING("⚠️ Skipping row with missing code or label"))
                    continue

                gender, created_flag = Gender.objects.get_or_create(
                    code=code,
                    defaults={
                        "label": label,
                        "position": idx
                    }
                )

                if not created_flag:
                    updated = False

                    if gender.label != label:
                        gender.label = label
                        updated = True

                    if gender.position != idx:
                        gender.position = idx
                        updated = True

                    if updated:
                        gender.save()
                        self.stdout.write(self.style.WARNING(f"[UPDATED] {label} ({code})"))
                    else:
                        skipped += 1
                        self.stdout.write(f"[SKIPPED] {label} ({code}) already exists")
                else:
                    created += 1
                    self.stdout.write(self.style.SUCCESS(f"[CREATED] {label} ({code})"))

        self.stdout.write(self.style.SUCCESS(f"\n✅ Created: {created}"))
        self.stdout.write(self.style.WARNING(f"⚠️ Skipped (existing or updated): {skipped}"))
