# apps > user_profiles > admin.py

from django.contrib import admin
from django.utils.html import format_html

from apps.common.utils.ip_tracker import get_client_ip
from .models import (
    AgeRange,
    Gender,
    EducationLevel,
    ReferralSource,
    ResidencyType,
    CivicInterestArea,
    County,
    Constituency,
    Ward,
    UserProfile,
)
from apps.user_profiles.forms.profile_admin import UserProfileAdminForm


# -------------------------------------------------------------------------
# Demographic & Reference Data Admins
# -------------------------------------------------------------------------

@admin.register(AgeRange)
class AgeRangeAdmin(admin.ModelAdmin):
    list_display = ("position", "label", "code")
    list_display_links = ("label",)
    list_editable = ("position",)
    ordering = ("position",)
    search_fields = ("code", "label")
    list_per_page = 25


@admin.register(Gender)
class GenderAdmin(admin.ModelAdmin):
    list_display = ("position", "code", "label")
    list_display_links = ("code", "label")
    list_editable = ("position",)
    ordering = ("position",)
    search_fields = ("code", "label")
    list_per_page = 25


@admin.register(EducationLevel)
class EducationLevelAdmin(admin.ModelAdmin):
    list_display = ("position", "code", "label")
    list_display_links = ("code", "label")
    list_editable = ("position",)
    ordering = ("position",)
    search_fields = ("code", "label")
    list_per_page = 25


@admin.register(ReferralSource)
class ReferralSourceAdmin(admin.ModelAdmin):
    list_display = ("position", "code", "label", "category")
    list_display_links = ("code", "label")
    list_editable = ("position",)
    list_filter = ("category",)
    search_fields = ("code", "label", "category")
    ordering = ("position",)
    list_per_page = 25


@admin.register(ResidencyType)
class ResidencyTypeAdmin(admin.ModelAdmin):
    list_display = ("position", "code", "label")
    list_display_links = ("code", "label")
    list_editable = ("position",)
    ordering = ("position",)
    search_fields = ("code", "label")
    list_per_page = 25


@admin.register(CivicInterestArea)
class CivicInterestAreaAdmin(admin.ModelAdmin):
    list_display = ("code", "label", "description", "icon")
    list_display_links = ("code", "label")
    search_fields = ("code", "label", "description")
    ordering = ("label",)
    list_per_page = 25


@admin.register(County)
class CountyAdmin(admin.ModelAdmin):
    list_display = ("code", "name")
    list_display_links = ("code", "name")
    search_fields = ("code", "name")
    ordering = ("code",)
    list_per_page = 25


@admin.register(Constituency)
class ConstituencyAdmin(admin.ModelAdmin):
    list_display = ("name", "county")
    list_display_links = ("name",)
    search_fields = ("name", "county__name", "county__code")
    list_filter = ("county",)
    ordering = ("county__code", "name")
    list_per_page = 25


@admin.register(Ward)
class WardAdmin(admin.ModelAdmin):
    list_display = ("name", "constituency", "get_county", "latitude", "longitude")
    list_display_links = ("name",)
    search_fields = ("name", "constituency__name", "constituency__county__name")
    list_filter = ("constituency__county", "constituency")
    ordering = ("constituency__county__code", "constituency__name", "name")
    list_per_page = 25

    def get_county(self, obj):
        return obj.constituency.county.name
    get_county.short_description = "County"


# -------------------------------------------------------------------------
# Enhanced UserProfile Admin
# -------------------------------------------------------------------------

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Admin config for UserProfile with thumbnail, progress bar,
    grouped fieldsets, search, filters, and autocomplete.
    """
    form = UserProfileAdminForm

    list_display = (
        "user",
        "profile_image_thumb",
        "completion_bar",
        "age_range",
        "gender",
        "education_level",
        "registered_at",
        "last_wizard_login_at",
    )
    list_select_related = (
        "user",
        "age_range",
        "gender",
        "education_level",
        "county",
        "constituency",
        "ward",
    )
    search_fields = ("user__username", "user__email", "whatsapp_opt_in_number")
    list_filter = (
        "gender",
        "education_level",
        "residency_type",
        "county",
        "wants_bill_notifications",
    )

    readonly_fields = (
        "profile_image_thumb",
        "completion_percentage",
        "registered_at",
        "registration_ip",
        "country_from_phone_code",
        "last_wizard_login_at",  
    )
    
    autocomplete_fields = (
        "user",
        "age_range",
        "gender",
        "education_level",
        "residency_type",
        "referral_source",
        "civic_interest_areas",
        "county",
        "constituency",
        "ward",
        "county_of_origin",
    )
    fieldsets = (
        (None, {
            "fields": ("user", "profile_image_thumb", "profile_image"),
        }),
        ("Demographics", {
            "fields": (
                "age_range",
                "gender",
                "education_level",
                "residency_type",
                "referral_source",
            ),
        }),
        ("Civic Geography", {
            "fields": (
                "county",
                "constituency",
                "ward",
                "county_of_origin",
                "current_country_of_residence",
            ),
        }),
        ("Interests & Participation", {
            "fields": (
                "civic_interest_areas",
                "has_voted_before",
                "knows_voting_process",
                "wants_bill_notifications",
            ),
        }),
        ("Contact & Metadata", {
            "fields": (
                "country_from_phone_code",
                "whatsapp_opt_in_number",
                "registered_at",
                "registration_ip",
                "last_wizard_login_at", 
            ),
        }),
        ("Completion", {
            "classes": ("collapse",),
            "fields": ("completion_percentage",),
        }),
    )

    def profile_image_thumb(self, obj):
        if obj.profile_image:
            return format_html(
                '<img src="{}" width="40" height="40" style="object-fit:cover; border-radius:50%;" />',
                obj.profile_image.url
            )
        return format_html('<span style="color:#999;">—</span>')
    profile_image_thumb.short_description = "Photo"

    def completion_bar(self, obj):
        pct = obj.completion_percentage
        return format_html(
            '<div style="background:#f0f0f0; border-radius:3px; width:100px; height:10px; overflow:hidden;">'
            '<div style="background:#5cb85c; width:{}%; height:100%;"></div>'
            '</div> <strong>{}%</strong>',
            pct,
            pct
        )
    completion_bar.short_description = "Profile %"

    def save_model(self, request, obj, form, change):
        # capture IP when creating via admin UI
        if not change:
            obj.registration_ip = get_client_ip(request)
        super().save_model(request, obj, form, change)
