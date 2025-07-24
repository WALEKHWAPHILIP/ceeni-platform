from django.db import models


# ------------------------------------------------------------------------------
# County Model
# ------------------------------------------------------------------------------

class County(models.Model):
    """
    Represents one of Kenya's 47 administrative counties.

    Fields:
    - code: 3-digit official string code (e.g., '001' for Mombasa)
    - name: Human-readable county name (e.g., 'Mombasa')
    """

    code = models.CharField(
        max_length=3,
        unique=True,
        help_text="Official 3-digit county code (e.g., '047')"
    )

    name = models.CharField(
        max_length=64,
        unique=True,
        help_text="County name (e.g., 'Nairobi')"
    )

    class Meta:
        ordering = ["code"]
        verbose_name = "County"
        verbose_name_plural = "Counties"

    def __str__(self):
        return self.name


# ------------------------------------------------------------------------------
# Constituency Model
# ------------------------------------------------------------------------------

class Constituency(models.Model):
    """
    Represents an electoral constituency within a county.

    Fields:
    - name: Constituency name (e.g., 'Lang’ata')
    - county: ForeignKey to the parent County
    """

    name = models.CharField(
        max_length=64,
        help_text="Constituency name (e.g., 'Lang’ata')"
    )

    county = models.ForeignKey(
        County,
        on_delete=models.CASCADE,
        related_name="constituencies"
    )

    class Meta:
        unique_together = ("name", "county")
        ordering = ["county__code", "name"]
        verbose_name = "Constituency"
        verbose_name_plural = "Constituencies"

    def __str__(self):
        return f"{self.name} — {self.county.name}"


# ------------------------------------------------------------------------------
# Ward Model
# ------------------------------------------------------------------------------

class Ward(models.Model):
    """
    Represents a ward (sub-constituency unit) in Kenya’s electoral map.

    Fields:
    - name: Ward name (e.g., 'South B')
    - constituency: ForeignKey to parent Constituency
    - latitude, longitude: Optional location data for mapping
    """

    name = models.CharField(
        max_length=64,
        help_text="Ward name (e.g., 'South B')"
    )

    constituency = models.ForeignKey(
        Constituency,
        on_delete=models.CASCADE,
        related_name="wards"
    )

    latitude = models.FloatField(
        null=True, blank=True,
        help_text="Latitude coordinate for the ward (if known)"
    )

    longitude = models.FloatField(
        null=True, blank=True,
        help_text="Longitude coordinate for the ward (if known)"
    )

    class Meta:
        unique_together = ("name", "constituency")
        ordering = ["constituency__county__code", "constituency__name", "name"]
        verbose_name = "Ward"
        verbose_name_plural = "Wards"

    def __str__(self):
        return f"{self.name} — {self.constituency.name}, {self.constituency.county.name}"
