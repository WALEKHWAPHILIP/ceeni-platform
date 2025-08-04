# apps > user_profiles > models > profile.py

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
    # Cached completion percentage (0–100)
    # --------------------------------------------------------------------------
    completion_percentage = models.PositiveSmallIntegerField(
        default=0,
        editable=False,
        db_index=True,
        help_text="Snapshot of profile completion (0–100)."
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

    # --------------------------------------------------
    # Track last time user resumed profile wizard
    # --------------------------------------------------
    last_wizard_login_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Timestamp of last time user returned to resume an incomplete profile."
    )
    

    # --------------------------------------------------------------------------
    # Model validation
    # --------------------------------------------------------------------------
    def clean(self):
        """
        Validates hierarchical consistency between county → constituency → ward.
        """
        if self.constituency and self.county and self.constituency.county != self.county:
            raise ValidationError("Selected constituency does not belong to the selected county.")
        if self.ward and self.constituency and self.ward.constituency != self.constituency:
            raise ValidationError("Selected ward does not belong to the selected constituency.")

    def __str__(self):
        return f"Profile of {self.user.username}"



    # =============================
    # Profile Completion Utilities
    # =============================

    def calculate_completion(self) -> int:
        """
        Calculates percentage of completed profile fields.
        - Treats BooleanFields like has_voted_before and wants_bill_notifications
        as complete even when False (i.e., valid 'No' answer).
        - Only counts ManyToMany fields if profile instance exists (has PK).
        """
        scalar_fields = [
            'age_range', 'gender', 'education_level',
            'residency_type', 'referral_source',
            'county', 'constituency', 'ward',
            'county_of_origin', 'current_country_of_residence',
            'has_voted_before', 'knows_voting_process',
            'wants_bill_notifications', 'profile_image',
        ]

        filled = 0
        for field in scalar_fields:
            value = getattr(self, field, None)

            # Treat False as a valid (filled) value — do NOT count only truthy
            if value is not None and value != '':
                filled += 1

        # Count civic_interest_areas (M2M) only if profile has been saved
        if self.pk and self.civic_interest_areas.exists():
            filled += 1

        total = len(scalar_fields) + 1  # +1 for the M2M field
        return int((filled / total) * 100)


    def save(self, *args, **kwargs):
        """
        Override save to recalculate and persist completion_percentage.
        """
        new_pct = self.calculate_completion()
        if new_pct != self.completion_percentage:
            self.completion_percentage = new_pct
        super().save(*args, **kwargs)
        
    # =============================
    # Completion Status Utility
    # =============================
    def is_complete(self) -> bool:
        """
        Returns True if the user's profile is 100% complete.
        This uses the cached 'completion_percentage' field,
        which is updated automatically on save().

        Use this method to redirect users based on completion status:
        e.g., incomplete users → profile wizard, complete users → dashboard.
        """
        return self.completion_percentage == 100
    

    # =============================
    # Profile Wizard Screen Mapping
    # =============================
    SCREEN_FIELD_MAP: list[tuple[str, list[str]]] = [
        ('user_profiles:screen_1', ['age_range', 'gender', 'education_level']),
        ('user_profiles:screen_2', ['county', 'constituency', 'ward']),
        ('user_profiles:screen_3', ['county_of_origin', 'current_country_of_residence', 'residency_type']),
        ('user_profiles:screen_4', ['civic_interest_areas', 'has_voted_before', 'knows_voting_process']),
        ('user_profiles:screen_5', ['wants_bill_notifications', 'whatsapp_opt_in_number']),
        ('user_profiles:screen_6', ['referral_source']),
        # screen_7 is assumed final confirmation
    ]


    # =============================
    # Next Step Resolution Utility
    # =============================
    def get_next_incomplete_screen(self) -> str:
        """
        Determines the next screen based on missing profile fields.
        Handles special logic like optional WhatsApp number.
        """
        for screen_name, fields in self.SCREEN_FIELD_MAP:
            for field in fields:
                value = getattr(self, field, None)

                # Special case: civic_interest_areas (M2M)
                if hasattr(value, 'exists') and not value.exists():
                    return screen_name

                # Special case: whatsapp number is only required if user opted in
                if field == 'whatsapp_opt_in_number':
                    wants = getattr(self, 'wants_bill_notifications', None)
                    if wants is True and not value:
                        return screen_name
                    # If wants is False or None, empty number is fine
                    continue

                # Normal fields: treat None, '', [], but NOT False, as missing
                if value in [None, '', []]:
                    return screen_name

        return 'user_profiles:screen_7'

    
        

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
