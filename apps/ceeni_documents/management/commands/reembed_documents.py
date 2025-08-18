from django.core.management.base import BaseCommand
from django.db import transaction

# Project-style imports (absolute path per project convention)
from apps.ceeni_documents.models import Section, Embedding
from apps.ceeni_documents.services.embedder import embed_texts, MODEL_NAME


class Command(BaseCommand):
    """
    Management command: Recompute embeddings for all Section records.

    This is useful when:
    - The embedding model changes (MODEL_NAME updated)
    - Embedding parameters change
    - Embedding data is missing/corrupted

    For each Section:
    - If an Embedding row exists, it is updated.
    - If missing, it is created.
    """

    help = "Recompute embeddings for all sections (updates or creates Embedding rows)."

    def add_arguments(self, parser):
        # Batch size controls number of sections embedded per API call
        parser.add_argument(
            "--batch",
            type=int,
            default=128,
            help="Embedding batch size. Tune for API/memory performance."
        )

    def handle(self, *args, **options):
        batch = options["batch"]

        # Select all sections, including any related embedding for efficiency
        qs = Section.objects.select_related("embedding").order_by("id")
        total = qs.count()

        if total == 0:
            self.stdout.write("No sections found.")
            return

        self.stdout.write(self.style.MIGRATE_HEADING(
            f"Re-embedding {total} section(s) with model={MODEL_NAME}, batch={batch}"
        ))

        buf_texts = []     # buffer of text chunks to embed
        buf_sections = []  # matching Section objects

        def flush():
            """
            Process the current buffer:
            - Generate embeddings for buffered texts
            - Create or update Embedding objects in a single DB transaction
            """
            if not buf_texts:
                return

            vecs = embed_texts(buf_texts)  # Call embedder service

            with transaction.atomic():
                for section, v in zip(buf_sections, vecs):
                    emb, _ = Embedding.objects.get_or_create(
                        section=section,
                        defaults={
                            "model": MODEL_NAME,
                            "vector": v.tobytes(),
                            "dim": int(v.shape[0]),
                        },
                    )
                    # Update vector/model/dim in case they have changed
                    emb.model = MODEL_NAME
                    emb.dim = int(v.shape[0])
                    emb.vector = v.tobytes()
                    emb.save()

            # Clear buffers after committing
            buf_texts.clear()
            buf_sections.clear()

        # Iterate through all sections using .iterator() for memory efficiency
        for section in qs.iterator():
            buf_texts.append(section.text)
            buf_sections.append(section)

            # Flush when batch size is reached
            if len(buf_texts) >= batch:
                flush()
                # Print lightweight progress indicator without newline
                self.stdout.write(".", ending="")

        # Flush any remaining buffered sections
        flush()

        self.stdout.write(self.style.SUCCESS("\nRe-embedding complete."))
