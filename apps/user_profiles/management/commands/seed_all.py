from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = "Seeds all reference models for CEENI platform in the correct order."

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE("Starting to seed all reference data..."))

        try:
            # ------------------------------
            # 1. DEMOGRAPHIC REFERENCE DATA
            # ------------------------------
            call_command("import_genders")              # Import gender options (e.g. Male, Female, Other)
            call_command("import_age_ranges")           # Import predefined age brackets
            call_command("import_education_levels")     # Import levels of education
            call_command("import_residency_types")      # Import types like urban, rural, etc.
            call_command("import_referral_sources")     # Import how users heard about the platform

            # ------------------------------
            # 2. CIVIC INTEREST AREAS
            # ------------------------------
            call_command("import_civic_interest_areas") # Import focus areas (e.g. healthcare, environment)

            # ------------------------------
            # 3. KENYAN LOCATION HIERARCHY
            # ------------------------------
            call_command("import_kenyan_locations")             # Seed all 47 counties, Seed constituencies linked to counties, Seed wards linked to constituencies

            # ------------------------------
            # **** ADD NEW IMPORT COMMANDS BELOW ****
            # ------------------------------
            # For example: call_command("import_languages")

            self.stdout.write(self.style.SUCCESS("✅ All seed data imported successfully."))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f"❌ Failed to seed: {str(e)}"))
