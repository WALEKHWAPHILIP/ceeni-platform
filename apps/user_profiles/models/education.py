from django.db import models


# ------------------------------------------------------------------------------
# EducationLevel Model
# ------------------------------------------------------------------------------

class EducationLevel(models.Model):
    """
    Represents standardized formal education levels for user classification.
    """

    position = models.PositiveIntegerField(
        default=0,
        help_text="Controls display order (lower = higher priority)"
    )

    code = models.CharField(
        max_length=32,
        unique=True,
        help_text="Machine-readable slug (e.g., 'secondary_completed')"
    )

    label = models.CharField(
        max_length=64,
        help_text="Human-readable education level (e.g. 'Secondary Completed')"
    )

    class Meta:
        ordering = ["position"]
        verbose_name = "Education Level"
        verbose_name_plural = "Education Levels"

    def __str__(self):
        return self.label

