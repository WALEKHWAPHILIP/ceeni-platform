from django.db import models

class Embedding(models.Model):
    """
    Stores vector embeddings for a Section.
    Uses string reference for Section to avoid circular imports.
    """
    section = models.OneToOneField(
        "ceeni_documents.Section",
        on_delete=models.CASCADE,
        related_name="embedding"
    )
    model = models.CharField(max_length=128)
    vector = models.BinaryField()  # store float32 array via np.tobytes()
    dim = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=["model"])]

    def __str__(self):
        return f"Embedding for section {self.section.id} using model {self.model}"
