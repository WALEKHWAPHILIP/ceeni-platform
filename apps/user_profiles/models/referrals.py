from django.db import models




# ------------------------------------------------------------------------------
# ReferralSource Model
# ------------------------------------------------------------------------------

class ReferralSource(models.Model):
    """
    Describes how a user learned about CEENI — e.g., 'Facebook', 'Friend', 'Baraza'.
    """

    code = models.CharField(
        max_length=32,
        unique=True,
        help_text="Internal slug (e.g., 'facebook', 'radio', 'public_baraza')"
    )

    label = models.CharField(
        max_length=64,
        help_text="Display label (e.g., 'Friend or Family', 'Flyer or Poster')"
    )

    category = models.CharField(
        max_length=32,
        blank=True,
        help_text="Optional grouping (e.g., 'Media', 'Offline', 'Partner')"
    )

    position = models.PositiveSmallIntegerField(
        default=0,
        help_text="Ordering index (lower = higher)"
    )

    class Meta:
        ordering = ["position", "label"]
        verbose_name = "Referral Source"
        verbose_name_plural = "Referral Sources"

    def __str__(self):
        return self.label


