from django.contrib import admin

from .models import (
    # ───────────────────────────────
    # Demographic models
    # ───────────────────────────────
    AgeRange,        # e.g., '18–24', '25–34'
    Gender,          # e.g., Male, Female, Nonbinary
    
    # ───────────────────────────────
    # User profile models
    # ───────────────────────────────
    UserProfile,     # Extended profile information per user

    # ───────────────────────────────
    # Reference data models
    # ───────────────────────────────
    EducationLevel,  # e.g., Primary, Secondary, Undergraduate
    ReferralSource,  # e.g., Facebook, Radio, Chief
    ResidencyType,   # e.g., Urban, Rural, Informal Settlement

    # ───────────────────────────────
    # Civic engagement
    # ───────────────────────────────
    CivicInterestArea,  # e.g., Elections, Health, Youth Rights

    # ───────────────────────────────
    # Location hierarchy
    # ───────────────────────────────
    County,          # Kenya's 47 official counties
    Constituency,    # Electoral constituencies within counties
    Ward,            # Sub-constituency administrative units
)


# -------------------------------------------------------------------------
# FORM: Attach custom admin form for UserProfile with cascading dropdowns
# -------------------------------------------------------------------------
# Enables dynamic filtering of Constituency and Ward fields based on
# selected County and Constituency respectively (via django-autocomplete-light)
from apps.user_profiles.forms.profile_admin import UserProfileAdminForm



# ------------------------------------------------------------------------------
# Admin Customization for AgeRange Model
# ------------------------------------------------------------------------------

@admin.register(AgeRange)
class AgeRangeAdmin(admin.ModelAdmin):
    """Admin config for AgeRange"""
    list_display = ("position", "label", "code")   # 'label' appears first as clickable
    list_display_links = ("label",)               # Only 'label' is clickable
    list_editable = ("position",)                 # Allow inline editing of 'position'
    ordering = ("position",)                      # Sort by 'position'
    search_fields = ("code", "label")             # Enable admin search
    list_per_page = 25

    fieldsets = (
        (None, {
            "fields": ("position", "code", "label"),
            "description": "Defines user age ranges for civic segmentation and insights."
        }),
    )


# ------------------------------------------------------------------------------
# Admin Customization for Gender Model
# ------------------------------------------------------------------------------

@admin.register(Gender)
class GenderAdmin(admin.ModelAdmin):
    """Admin config for Gender"""
    list_display = ("position", "code", "label")   # Show position and identifiers
    list_display_links = ("code", "label")         # Allow clicking on code or label
    list_editable = ("position",)                  # Inline editing of 'position'
    search_fields = ("code", "label")              # Searchable fields
    ordering = ("position",)
    list_per_page = 25

    fieldsets = (
        (None, {
            "fields": ("position", "code", "label"),
            "description": "Manage gender options and their display order."
        }),
    )



# ------------------------------------------------------------------------------
# Admin Customization for EducationLevel Model
# ------------------------------------------------------------------------------

@admin.register(EducationLevel)
class EducationLevelAdmin(admin.ModelAdmin):
    """Admin config for EducationLevel"""
    list_display = ("position", "code", "label")       # Show position first
    list_display_links = ("code", "label")             # Make 'code' or 'label' clickable (not 'position')
    list_editable = ("position",)                      # Allow editing 'position' directly
    search_fields = ("code", "label")
    ordering = ("position",)
    list_per_page = 25

    fieldsets = (
        (None, {
            "fields": ("position", "code", "label"),
            "description": "Define recognized education levels for user classification."
        }),
    )


# ------------------------------------------------------------------------------
# Admin Customization for ReferralSource Model
# ------------------------------------------------------------------------------

@admin.register(ReferralSource)
class ReferralSourceAdmin(admin.ModelAdmin):
    """Admin config for ReferralSource"""
    list_display = ("position", "code", "label", "category")
    list_display_links = ("code", "label")             # Allows clicking on code or label
    list_editable = ("position",)                      # Editable 'position' field
    list_filter = ("category",)                        # Sidebar filter by category
    search_fields = ("code", "label", "category")
    ordering = ("position",)
    list_per_page = 25

    fieldsets = (
        (None, {
            "fields": ("position", "code", "label", "category"),
            "description": "Manage structured referral sources with category and order."
        }),
    )



# ------------------------------------------------------------------------------
# Admin Customization for ResidencyType Model
# ------------------------------------------------------------------------------

@admin.register(ResidencyType)
class ResidencyTypeAdmin(admin.ModelAdmin):
    """Admin config for ResidencyType"""
    list_display = ("position", "code", "label")        # Show sortable fields
    list_display_links = ("code", "label")              # 'code' or 'label' clickable
    list_editable = ("position",)                       # Inline editing of 'position'
    search_fields = ("code", "label")                   # Admin search
    ordering = ("position",)
    list_per_page = 25

    fieldsets = (
        (None, {
            "fields": ("position", "code", "label"),
            "description": (
                "Define residential environment types (e.g., Urban, Rural, Informal Settlement). "
                "Used to segment users and tailor civic access strategies."
            ),
        }),
    )


# ------------------------------------------------------------------------------
# Admin Customization for CivicInterestArea Model
# ------------------------------------------------------------------------------

@admin.register(CivicInterestArea)
class CivicInterestAreaAdmin(admin.ModelAdmin):
    """Admin config for Civic Interest Area"""

    list_display = ("code", "label",  "description", "icon")          # Show core identifiers
    list_display_links = ("code", "label")            # Clickable fields
    search_fields = ("code", "label", "description")  # Make it easy to find
    ordering = ("label",)
    list_per_page = 25

    fieldsets = (
        (None, {
            "fields": ("code", "label", "description", "icon"),
            "description": (
                "Manage CEENI civic interest areas. These drive personalization, "
                "civic engagement tagging, and user interest filtering."
            )
        }),
    )



### LOCATIONS

# ------------------------------------------------------------------------------
# Admin Customization for County Model
# ------------------------------------------------------------------------------

@admin.register(County)
class CountyAdmin(admin.ModelAdmin):
    """Admin config for County"""
    list_display = ("code", "name")
    list_display_links = ("code", "name")
    search_fields = ("code", "name")
    ordering = ("code",)
    list_per_page = 25

    fieldsets = (
        (None, {
            "fields": ("code", "name"),
            "description": "Kenya's 47 counties with official 3-digit codes"
        }),
    )


# ------------------------------------------------------------------------------
# Admin Customization for Constituency Model
# ------------------------------------------------------------------------------

@admin.register(Constituency)
class ConstituencyAdmin(admin.ModelAdmin):
    """Admin config for Constituency"""
    list_display = ("name", "county")
    list_display_links = ("name",)
    search_fields = ("name", "county__name", "county__code")
    list_filter = ("county",)
    ordering = ("county__code", "name")
    list_per_page = 25

    fieldsets = (
        (None, {
            "fields": ("county", "name"),
            "description": "Electoral constituencies nested within counties"
        }),
    )


# ------------------------------------------------------------------------------
# Admin Customization for Ward Model
# ------------------------------------------------------------------------------

@admin.register(Ward)
class WardAdmin(admin.ModelAdmin):
    """Admin config for Ward"""
    list_display = ("name", "constituency", "get_county", "latitude", "longitude")
    list_display_links = ("name",)
    search_fields = ("name", "constituency__name", "constituency__county__name")
    list_filter = ("constituency__county", "constituency")
    ordering = ("constituency__county__code", "constituency__name", "name")
    list_per_page = 25

    fieldsets = (
        (None, {
            "fields": ("constituency", "name", "latitude", "longitude"),
            "description": "Kenya's wards — the smallest electoral unit"
        }),
    )

    def get_county(self, obj):
        return obj.constituency.county.name
    get_county.short_description = "County"


# ------------------------------------------------------------------------------
# Admin Customization for UserProfile Model
# ------------------------------------------------------------------------------

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    
    form = UserProfileAdminForm  # Attach custom form with Select2 autocomplete widgets for location fields

    list_display = ("user", "age_range", "gender", "education_level", "registered_at")
    search_fields = ("user__username", "user__phone_number")
    list_filter = ("age_range", "gender", "education_level", "county", "constituency")

    readonly_fields = ("registered_at", "registration_ip", "country_from_phone_code")

    autocomplete_fields = (
        "user",
        "age_range",
        "gender",
        "education_level",
        "residency_type",
        "referral_source",
        "civic_interest_areas",
        "ward",
        "constituency",
        "county",
        "county_of_origin"
    )
