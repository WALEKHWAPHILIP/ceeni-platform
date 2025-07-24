import csv
from django.core.management.base import BaseCommand
from apps.common.models import BlockedNickname
from config.settings.base import CSV_DATA_DIR

class Command(BaseCommand):
    help = "Imports blocked nicknames from CSV (column: word)"

    def handle(self, *args, **kwargs):
        filepath = CSV_DATA_DIR / "blocked_nicknames.csv"
        created_count = 0
        skipped_count = 0

        with open(filepath, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                word = row.get("word", "").strip().lower()
                if not word:
                    continue

                blocked, created = BlockedNickname.objects.get_or_create(word=word)

                if created:
                    self.stdout.write(self.style.SUCCESS(f"[CREATED] {word}"))
                    created_count += 1
                else:
                    self.stdout.write(f"[SKIPPED] {word}")
                    skipped_count += 1

        self.stdout.write(f"\n✅ Created: {created_count}")
        self.stdout.write(f"⚠️ Skipped (already exists): {skipped_count}")