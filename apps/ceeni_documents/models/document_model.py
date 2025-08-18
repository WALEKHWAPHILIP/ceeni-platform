from django.db import models

class Document(models.Model):
    """
    Model representing a Document with different document types.
    """
    DOC_TYPES = [
        ("constitution", "Constitution"),
        ("bill", "Bill"),
        ("brief", "Brief"),
        ("other", "Other"),
    ]
    
    title = models.CharField(max_length=512)
    slug = models.SlugField(max_length=512, unique=True)
    doc_type = models.CharField(max_length=32, choices=DOC_TYPES, default="other")
    source_path = models.TextField(help_text="Original file path or URL")
    published_at = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
