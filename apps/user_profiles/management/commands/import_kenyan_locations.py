# ------------------------------------------------------------------------------
# CEENI Command: Import County → Constituency → Ward hierarchy from CSV
# ------------------------------------------------------------------------------

import csv
from collections import defaultdict
from django.core.management.base import BaseCommand
from django.conf import settings

from apps.user_profiles.models.locations import County, Constituency, Ward


class Command(BaseCommand):
    """Import the full Kenyan location hierarchy from official CSV files."""

    help = "Import counties, constituencies, and wards from structured CSV data"

    def handle(self, *args, **options):
        counties_path = settings.CSV_DATA_DIR / "counties.csv"
        locations_path = settings.CSV_DATA_DIR / "kenya_county_constituency_ward_latitude_longitude.csv"

        if not counties_path.exists() or not locations_path.exists():
            self.stderr.write(self.style.ERROR("❌ One or more CSV files not found."))
            return

        # ----------------------------------------------------------------------
        # Step 1: Load County Code Lookup from counties.csv
        # ----------------------------------------------------------------------
        county_lookup = {}

        with open(counties_path, newline='', encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row.get("name", "").strip()
                code = row.get("code", "").strip().zfill(3)
                if name and code:
                    county_lookup[name] = code

        # Validate lookup
        if not county_lookup:
            self.stderr.write(self.style.ERROR("❌ No valid counties found in counties.csv"))
            return

        # ----------------------------------------------------------------------
        # Step 2: Import Main Hierarchy from long CSV
        # ----------------------------------------------------------------------
        created = defaultdict(int)
        skipped = 0

        with open(locations_path, newline='', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)

            for row in reader:
                county_name = row["County"].strip()
                constituency_name = row["Constituency"].strip()
                ward_name = row["Ward"].strip()
                lat = row.get("Latitude", "").strip()
                lng = row.get("Longitude", "").strip()

                if not all([county_name, constituency_name, ward_name]):
                    self.stderr.write(self.style.WARNING("⚠️ Skipping row with missing data"))
                    skipped += 1
                    continue

                # Get code from lookup, fallback to "000"
                county_code = county_lookup.get(county_name, "000")

                county, _ = County.objects.get_or_create(
                    name=county_name,
                    defaults={"code": county_code}
                )

                constituency, _ = Constituency.objects.get_or_create(
                    name=constituency_name,
                    county=county
                )

                ward, created_flag = Ward.objects.get_or_create(
                    name=ward_name,
                    constituency=constituency,
                    defaults={
                        "latitude": float(lat) if lat else None,
                        "longitude": float(lng) if lng else None
                    }
                )

                if created_flag:
                    created["ward"] += 1
                    self.stdout.write(self.style.SUCCESS(f"[CREATED] {ward.name} → {constituency.name}, {county.name}"))
                else:
                    skipped += 1

        # ----------------------------------------------------------------------
        # Summary Output
        # ----------------------------------------------------------------------
        self.stdout.write(self.style.SUCCESS(f"\n✅ Wards Created: {created['ward']}"))
        self.stdout.write(self.style.WARNING(f"⚠️ Skipped (existing or missing): {skipped}"))
