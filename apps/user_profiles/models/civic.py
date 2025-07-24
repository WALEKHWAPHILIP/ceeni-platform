from django.db import models

# ------------------------------------------------------------------------------
# Section 3: Civic Interest Area Model
# ------------------------------------------------------------------------------

class CivicInterestArea(models.Model):
    """
    Represents a civic issue/topic that users care about or follow.

    Example Use Cases:
    - Personalization of civic education content.
    - User filtering by interest (e.g., health, elections, youth rights).
    - Tagging and classifying CEENI campaigns and reports.
    
    Fields:
    - code: A unique, URL-safe identifier used in internal logic, URLs, or APIs.
    - label: The human-readable display name shown to users.
    - description: Optional rich explanation for admin UIs or frontend tooltips.
    - icon: Optional UI enhancement (e.g., a FontAwesome or Material icon class).
    
    Why this model:
    - Keeps civic themes flexible and data-driven (no hardcoding in forms).
    - Enables deep analytics on interest-based engagement.
    - Decouples display logic from system logic (label ≠ code).
    """

    code = models.CharField(
        max_length=32,
        unique=True,
        help_text="Machine-friendly code (e.g., 'elections') used in filters and URLs"
    )

    label = models.CharField(
        max_length=64,
        help_text="Human-readable display name (e.g., 'Elections & Voting')"
    )

    description = models.TextField(
        blank=True,
        help_text="Optional description for tooltips, dashboards, or civic education modules"
    )

    icon = models.CharField(
        max_length=64,
        blank=True,
        help_text="Optional FontAwesome or custom icon class (e.g., 'fa-vote-yea')"
    )

    class Meta:
        ordering = ["label"]  # Ensures consistent display order alphabetically
        verbose_name = "Civic Interest Area"
        verbose_name_plural = "Civic Interest Areas"

    def __str__(self):
        # Returns the display label in admin listings, dropdowns, etc.
        return self.label
