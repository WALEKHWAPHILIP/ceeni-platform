import csv
from django.core.management.base import BaseCommand
from apps.user_profiles.models import AgeRange
from config.settings.base import CSV_DATA_DIR

class Command(BaseCommand):
    help = "Imports age ranges from CSV (code, label), assigns position by row order"

    def handle(self, *args, **kwargs):
        filepath = CSV_DATA_DIR / "age_ranges.csv"
        created_count = 0
        skipped_count = 0

        with open(filepath, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for idx, row in enumerate(reader):
                code = row["code"].strip()
                label = row["label"].strip()
                position = idx + 1

                age_range, created = AgeRange.objects.get_or_create(
                    code=code,
                    defaults={
                        "label": label,
                        "position": position
                    }
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(f"[CREATED] {label} ({code})"))
                    created_count += 1
                else:
                    # Update label and position if they differ
                    updated = False
                    if age_range.label != label:
                        age_range.label = label
                        updated = True
                    if age_range.position != position:
                        age_range.position = position
                        updated = True
                    if updated:
                        age_range.save()
                        self.stdout.write(self.style.WARNING(f"[UPDATED] {label} ({code})"))
                    else:
                        self.stdout.write(f"[SKIPPED] {label} ({code})")
                    skipped_count += 1

        self.stdout.write(f"\n✅ Created: {created_count}")
        self.stdout.write(f"⚠️ Skipped/Updated: {skipped_count}")
