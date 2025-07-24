from django.db import models


# ------------------------------------------------------------------------------
# AgeRange Model
# ------------------------------------------------------------------------------

class AgeRange(models.Model):
    """
    Represents standardized age brackets for user classification.
    Examples: '18–24', '25–34', '35–49'
    """

    code = models.CharField(
        max_length=32,
        unique=True,
        null=True,
        help_text="Machine-readable slug (e.g., 'age_18_24')"
    )

    label = models.CharField(
        max_length=50,
        unique=True,
        help_text="Display label for age bracket (e.g., '18–24')"
    )

    position = models.PositiveIntegerField(
        null=True,
        help_text="Ordering position (lower appears first in dropdowns)"
    )

    class Meta:
        ordering = ["position"]
        verbose_name = "Age Range"
        verbose_name_plural = "Age Ranges"

    def __str__(self):
        return self.label


# ------------------------------------------------------------------------------
# Gender Model
# ------------------------------------------------------------------------------

class Gender(models.Model):
    """
    Represents a user's self-identified gender.
    Supports flexibility and inclusion (e.g., Male, Female, Nonbinary, Prefer not to say).
    """

    code = models.CharField(
        max_length=32,
        unique=True,
        null=True,
        help_text="Machine-readable gender code (e.g., 'female', 'male', 'other')"
    )

    label = models.CharField(
        max_length=64,
        help_text="Display name (e.g., 'Female', 'Male', 'Other')"
    )

    position = models.PositiveSmallIntegerField(
        default=0,
        help_text="Controls display order in dropdowns and filters"
    )

    class Meta:
        ordering = ["position", "label"]
        verbose_name = "Gender"
        verbose_name_plural = "Genders"

    def __str__(self):
        return self.label
