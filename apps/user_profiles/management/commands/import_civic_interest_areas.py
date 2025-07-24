# ------------------------------------------------------------------------
# CEENI Command: Import Civic Interest Areas from CSV
# ------------------------------------------------------------------------

import csv
from django.core.management.base import BaseCommand
from django.conf import settings
from apps.user_profiles.models.civic import CivicInterestArea


class Command(BaseCommand):
    """CLI tool to import civic interest areas from a CSV file."""

    help = "Import civic interest areas from data/csv/civic_interest_areas.csv"

    def handle(self, *args, **options):
        csv_path = settings.CSV_DATA_DIR / "civic_interest_areas.csv"

        if not csv_path.exists():
            self.stderr.write(self.style.ERROR(f"❌ File not found at: {csv_path}"))
            return

        created, updated, skipped = 0, 0, 0

        with open(csv_path, newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                code = row.get("code", "").strip()
                label = row.get("label", "").strip()
                description = row.get("description", "").strip()
                icon = row.get("icon", "").strip()

                if not code or not label:
                    self.stderr.write(self.style.WARNING("⚠️ Skipping row with missing code or label"))
                    continue

                interest, created_flag = CivicInterestArea.objects.get_or_create(
                    code=code,
                    defaults={
                        "label": label,
                        "description": description,
                        "icon": icon
                    }
                )

                if not created_flag:
                    updated_flag = False

                    if interest.label != label:
                        interest.label = label
                        updated_flag = True
                    if interest.description != description:
                        interest.description = description
                        updated_flag = True
                    if interest.icon != icon:
                        interest.icon = icon
                        updated_flag = True

                    if updated_flag:
                        interest.save()
                        updated += 1
                        self.stdout.write(self.style.WARNING(f"[UPDATED] {label} ({code})"))
                    else:
                        skipped += 1
                        self.stdout.write(f"[SKIPPED] {label} ({code}) already up to date")
                else:
                    created += 1
                    self.stdout.write(self.style.SUCCESS(f"[CREATED] {label} ({code})"))

        # Summary
        self.stdout.write(self.style.SUCCESS(f"\n✅ Created: {created}"))
        self.stdout.write(self.style.WARNING(f"📝 Updated: {updated}"))
        self.stdout.write(self.style.NOTICE(f"⚠️ Skipped: {skipped}"))
