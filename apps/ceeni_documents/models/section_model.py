from django.db import models
from django.db.models import UniqueConstraint  # Import UniqueConstraint for modern unique constraints

class Section(models.Model):
    """
    Sections belonging to a Document, ordered by index.
    Uses a string reference for the Document to avoid circular imports.
    """
    document = models.ForeignKey(
        "ceeni_documents.Document",
        on_delete=models.CASCADE,
        related_name="sections"
    )
    index = models.PositiveIntegerField(default=0)
    heading = models.CharField(max_length=512, blank=True)
    text = models.TextField()
    meta = models.JSONField(default=dict, blank=True)

    class Meta:
        # Replace deprecated unique_together with UniqueConstraint for clarity and flexibility
        constraints = [
            UniqueConstraint(
                fields=["document", "index"], 
                name="unique_section_per_document_index"
            )
        ]
        ordering = ["document", "index"]

    def __str__(self):
        return f"Section {self.index} of {self.document.title}"
