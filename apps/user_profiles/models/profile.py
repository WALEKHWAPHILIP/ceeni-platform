from django.db import models
from django.contrib.auth import get_user_model
from django_countries.fields import CountryField
from django.core.exceptions import ValidationError

from apps.common.validators.identity import validate_phone_e164
from apps.user_profiles.models import (
    AgeRange,
    Gender,
    EducationLevel,
    ResidencyType,
    ReferralSource,
    CivicInterestArea,
    County,
    Constituency,
    Ward,
)

User = get_user_model()


# =============================
# User Profile Model Definition
# =============================

class UserProfile(models.Model):
    """
    Extended civic and demographic profile linked to a user.
    All fields are optional to support privacy-first and progressive onboarding.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # --------------------------------------------------------------------------
    # Profile image (optional, private by default)
    # --------------------------------------------------------------------------
    profile_image = models.ImageField(
        upload_to="user_profiles/profile_images/",
        null=True,
        blank=True,
        default="user_profiles/defaults/unisex_kenyan_flag.webp",
        verbose_name="Profile photo",
        help_text=(
            "Optional profile image. Only visible in your private dashboard. "
            "Default image shown if none is uploaded. "
            "Never shown publicly and will never be shared."
        )
    )


    # --------------------------------------------------------------------------
    # Demographic fields
    # --------------------------------------------------------------------------
    age_range = models.ForeignKey(AgeRange, null=True, blank=True, on_delete=models.SET_NULL)
    gender = models.ForeignKey(Gender, null=True, blank=True, on_delete=models.SET_NULL)
    education_level = models.ForeignKey(EducationLevel, null=True, blank=True, on_delete=models.SET_NULL)
    residency_type = models.ForeignKey(ResidencyType, null=True, blank=True, on_delete=models.SET_NULL)
    referral_source = models.ForeignKey(ReferralSource, null=True, blank=True, on_delete=models.SET_NULL)

    # --------------------------------------------------------------------------
    # Civic geography (progressive hierarchy: County → Constituency → Ward)
    # --------------------------------------------------------------------------
    county = models.ForeignKey(
        County,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="Select the county where you are registered as a voter."
    )

    constituency = models.ForeignKey(
        Constituency,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="Select your constituency (filtered based on county)."
    )

    ward = models.ForeignKey(
        Ward,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="Select your ward (filtered based on constituency)."
    )

    county_of_origin = models.ForeignKey(
        County,
        null=True,
        blank=True,
        related_name="profiles_originating_from",
        on_delete=models.SET_NULL,
        help_text="(Optional) County you consider your ancestral or cultural origin."
    )

    current_country_of_residence = CountryField(
        null=True,
        blank=True,
        help_text="Your current country of residence (optional if outside Kenya)."
    )

    # --------------------------------------------------------------------------
    # Civic engagement & interests
    # --------------------------------------------------------------------------
    civic_interest_areas = models.ManyToManyField(
        CivicInterestArea,
        blank=True,
        help_text="Select your key areas of civic interest (max 3–5 recommended)."
    )

    has_voted_before = models.BooleanField(
        null=True,
        blank=True,
        default=None,
        help_text="Let us know if you have voted before."
    )

    knows_voting_process = models.BooleanField(
        null=True,
        blank=True,
        default=None,
        help_text="Tell us if you understand how voting works."
    )


    wants_bill_notifications = models.BooleanField(
        null=True,
        blank=True,
        default=None,
        help_text=(
            "Would you like to be notified when major progress is made on the Ethnic Equity and Public Representation Bill, "
            "including voting stages, committee debates, and implementation milestones? "
            "If you choose to opt in, we’ll send periodic civic alerts via WhatsApp or SMS so you can follow the bill’s journey."
        )
    )


    # --------------------------------------------------------------------------
    # Contact & registration metadata
    # --------------------------------------------------------------------------
    country_from_phone_code = models.CharField(
        max_length=32,
        editable=False,
        default="undetermined"
    )


    whatsapp_opt_in_number = models.CharField(
        max_length=20,
        blank=True,
        validators=[validate_phone_e164],
        help_text=(
            "If you've opted to receive bill updates, please enter a valid WhatsApp number in international E.164 format "
            "(e.g., +254712345678). This is where we’ll send civic alerts via WhatsApp or SMS. "
            "Leave blank if you prefer not to receive notifications."
        )
    )

    registered_at = models.DateTimeField(auto_now_add=True)
    registration_ip = models.GenericIPAddressField(null=True, blank=True)

    # --------------------------------------------------------------------------
    # Model validation
    # --------------------------------------------------------------------------
    def clean(self):
        """
        Validates hierarchical consistency between county → constituency → ward.
        """
        if self.constituency and self.county:
            if self.constituency.county != self.county:
                raise ValidationError("Selected constituency does not belong to the selected county.")

        if self.ward and self.constituency:
            if self.ward.constituency != self.constituency:
                raise ValidationError("Selected ward does not belong to the selected constituency.")

    def __str__(self):
        return f"Profile of {self.user.username}"

    # =============================
    # Profile Completion Utilities
    # =============================

    # --- Civic Participation Completeness Check ---

    def has_required_profile_fields(self):
        """
        Returns True if the user has completed all mandatory profile fields
        required for participation in civic features like voting or commenting.
        """
        return all([
            self.age_range_id,
            self.gender_id,
            self.education_level_id,
            self.residency_type_id,
            self.referral_source_id,
            self.county_id,
            self.constituency_id,
            self.ward_id,
            self.county_of_origin_id,
            self.current_country_of_residence,
            self.civic_interest_areas.exists(),
            self.has_voted_before is not None,
            self.knows_voting_process is not None,
        ])

    # --- Profile Completion Percentage Calculator ---

    def completion_percentage(self):
        """
        Calculates the percentage of completed profile fields based on
        mandatory civic participation attributes (excluding optional ones).
        """
        fields = [
            'age_range',
            'gender',
            'education_level',
            'residency_type',
            'referral_source',
            'county',
            'constituency',
            'ward',
            'county_of_origin',
            'current_country_of_residence',
            'has_voted_before',
            'knows_voting_process',
        ]

        # Count how many of the above fields are filled (non-empty)
        filled = sum(1 for f in fields if getattr(self, f))

        # Count civic interest areas separately if at least one exists
        if self.civic_interest_areas.exists():
            filled += 1

        # Total fields measured: 13 + 1 (civic interest areas)
        return int((filled / (len(fields) + 1)) * 100)

    # =============================
    # Model Meta Configuration
    # =============================

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
