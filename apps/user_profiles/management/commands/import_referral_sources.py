# ------------------------------------------------------------------------------
# CEENI Command: Import Referral Sources from CSV
# ------------------------------------------------------------------------------

import csv
from django.core.management.base import BaseCommand
from django.conf import settings

# Modular import
from apps.user_profiles.models.referrals import ReferralSource


class Command(BaseCommand):
    """CLI tool to import structured referral sources from a CSV file."""

    help = "Import referral sources from data/csv/referral_sources.csv"

    def handle(self, *args, **options):
        # Path to CSV
        csv_path = settings.CSV_DATA_DIR / "referral_sources.csv"

        if not csv_path.exists():
            self.stderr.write(self.style.ERROR(f"❌ File not found at: {csv_path}"))
            return

        created, skipped = 0, 0

        # ----------------------------------------------------------------------
        # Read and import each referral source
        # ----------------------------------------------------------------------
        with open(csv_path, newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)

            for idx, row in enumerate(reader, start=1):
                code = row.get("code", "").strip()
                label = row.get("label", "").strip()
                category = row.get("category", "").strip()

                if not code or not label:
                    self.stderr.write(self.style.WARNING("⚠️ Skipping row with missing code or label"))
                    continue

                source, created_flag = ReferralSource.objects.get_or_create(
                    code=code,
                    defaults={
                        "label": label,
                        "category": category,
                        "position": idx,
                    }
                )

                if not created_flag:
                    updated = False

                    if source.label != label:
                        source.label = label
                        updated = True

                    if source.category != category:
                        source.category = category
                        updated = True

                    if source.position != idx:
                        source.position = idx
                        updated = True

                    if updated:
                        source.save()
                        self.stdout.write(self.style.WARNING(f"[UPDATED] {label} ({code})"))
                    else:
                        skipped += 1
                        self.stdout.write(f"[SKIPPED] {label} ({code}) already exists")
                else:
                    created += 1
                    self.stdout.write(self.style.SUCCESS(f"[CREATED] {label} ({code})"))

        # ----------------------------------------------------------------------
        # Final summary
        # ----------------------------------------------------------------------
        self.stdout.write(self.style.SUCCESS(f"\n✅ Created: {created}"))
        self.stdout.write(self.style.WARNING(f"⚠️ Skipped (existing or updated): {skipped}"))
