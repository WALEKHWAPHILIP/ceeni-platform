from django.db import models

# ------------------------------------------------------------------------------
# ResidencyType Model
# ------------------------------------------------------------------------------

class ResidencyType(models.Model):
    """
    Represents the user's type of living environment — e.g., Urban, Rural, Informal Settlement.
    Useful for equity insights and civic access modeling.
    """

    position = models.PositiveSmallIntegerField(
        default=0,
        help_text="Display order (lower = higher priority)"
    )

    code = models.CharField(
        max_length=32,
        unique=True,
        help_text="Machine-readable slug (e.g., 'urban', 'rural', 'nomadic')"
    )

    label = models.CharField(
        max_length=64,
        help_text="Display label for forms and admin (e.g., 'Urban')"
    )

    class Meta:
        ordering = ["position"]
        verbose_name = "Residency Type"
        verbose_name_plural = "Residency Types"

    def __str__(self):
        return self.label
