# ------------------------------------------------------------------------------
# CEENI Command: Import Residency Types from CSV
# ------------------------------------------------------------------------------

import csv
from django.core.management.base import BaseCommand
from django.conf import settings
from apps.user_profiles.models.residency import ResidencyType


class Command(BaseCommand):
    """CLI tool to import residency types from a CSV file into the database."""

    help = "Import residency types from data/csv/residency_types.csv"

    def handle(self, *args, **options):
        csv_path = settings.CSV_DATA_DIR / "residency_types.csv"

        if not csv_path.exists():
            self.stderr.write(self.style.ERROR(f"❌ File not found at: {csv_path}"))
            return

        created, skipped = 0, 0

        with open(csv_path, newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)

            for idx, row in enumerate(reader, start=1):
                code = row.get("code", "").strip()
                label = row.get("label", "").strip()

                if not code or not label:
                    self.stderr.write(self.style.WARNING("⚠️ Skipping row with missing code or label"))
                    continue

                residency, created_flag = ResidencyType.objects.get_or_create(
                    code=code,
                    defaults={
                        "label": label,
                        "position": idx,
                    }
                )

                if not created_flag:
                    updated = False

                    if residency.label != label:
                        residency.label = label
                        updated = True

                    if residency.position != idx:
                        residency.position = idx
                        updated = True

                    if updated:
                        residency.save()
                        self.stdout.write(self.style.WARNING(f"[UPDATED] {label} ({code})"))
                    else:
                        skipped += 1
                        self.stdout.write(f"[SKIPPED] {label} ({code}) already exists")
                else:
                    created += 1
                    self.stdout.write(self.style.SUCCESS(f"[CREATED] {label} ({code})"))

        self.stdout.write(self.style.SUCCESS(f"\n✅ Created: {created}"))
        self.stdout.write(self.style.WARNING(f"⚠️ Skipped (existing or updated): {skipped}"))
