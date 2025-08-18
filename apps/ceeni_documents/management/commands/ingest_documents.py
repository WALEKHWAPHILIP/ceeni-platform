from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils.text import slugify

from pathlib import Path
import hashlib

# Project-style imports (absolute paths per project convention)
from apps.ceeni_documents.models import Document, Section, Embedding
from apps.ceeni_documents.services.chunker import sentence_chunks
from apps.ceeni_documents.services.embedder import embed_texts, MODEL_NAME
from apps.ceeni_documents.services.parsers import parse_pdf, parse_docx, parse_html


def _normalize_for_hash(path_str: str) -> str:
    """
    Normalize a file path for deterministic hashing:
    - Converts Windows/Unix separators to POSIX style
    - Lowercases the path
    This ensures slug collision checks are OS-independent and case-insensitive.
    """
    return Path(path_str).as_posix().lower()


def _short_hash(s: str, n: int = 8) -> str:
    """
    Generate a short, deterministic hash for slug uniqueness.
    SHA-1 is used here (non-cryptographic purpose) to avoid collisions
    while keeping slugs human-readable. Default length is 8 chars.
    """
    return hashlib.sha1(s.encode("utf-8")).hexdigest()[:n]


# File extension to parser function mapping
# Allows adding new formats without modifying main ingestion logic
EXT_MAP = {
    ".pdf": lambda p: parse_pdf(p),
    ".docx": lambda p: parse_docx(p),
    ".html": lambda p: parse_html(p, is_html=False),
    ".htm": lambda p: parse_html(p, is_html=False),
    ".txt": lambda p: Path(p).read_text(encoding="utf-8", errors="ignore"),
}


class Command(BaseCommand):
    help = "Ingest files from a folder into Document/Section/Embedding."

    def add_arguments(self, parser):
        # Required: folder path to scan recursively for ingestable files
        parser.add_argument("folder", type=str, help="Folder to scan recursively.")

        # Document type for all ingested files (taxonomy control)
        parser.add_argument(
            "--doc-type",
            default="other",
            choices=["constitution", "bill", "brief", "other"],
            help="Document type to assign to all ingested files.",
        )

        # Idempotence control: clean re-ingest of existing document if --replace is set
        parser.add_argument(
            "--replace",
            action="store_true",
            help="If target document slug exists, delete its sections and re-ingest.",
        )

        # Chunking parameters for sentence_chunks()
        parser.add_argument("--max-chars", type=int, default=1400, help="Chunk size in characters.")
        parser.add_argument("--overlap", type=int, default=120, help="Chunk overlap in characters.")

        # Optional substring filter for selective ingestion
        parser.add_argument(
            "--pattern",
            type=str,
            default=None,
            help='Only ingest files whose path contains this substring (case-insensitive).',
        )

        # Safety: preview ingestion actions without DB writes
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="List what would be ingested without writing to the database.",
        )

    def handle(self, *args, **options):
        folder = options["folder"]
        doc_type = options["doc_type"]
        replace = options["replace"]
        max_chars = options["max_chars"]
        overlap = options["overlap"]
        pattern = (options["pattern"] or "").lower()
        dry = options["dry_run"]

        base = Path(folder)
        if not base.exists() or not base.is_dir():
            # Fail fast if target path is invalid
            raise CommandError(f"Folder not found or not a directory: {folder}")

        # Recursively find supported files
        files = [
            f for f in base.rglob("*")
            if f.is_file() and f.suffix.lower() in EXT_MAP
        ]

        # Optional pattern filtering
        if pattern:
            files = [f for f in files if pattern in str(f).lower()]

        self.stdout.write(self.style.MIGRATE_HEADING(f"Found {len(files)} file(s)"))

        for f in files:
            parse = EXT_MAP[f.suffix.lower()]

            # Step 1: Parse file into text
            try:
                text = parse(str(f))
            except Exception as e:
                # Log and skip parse errors
                self.stderr.write(self.style.ERROR(f"Parse failed: {f} — {e}"))
                continue

            if not (text or "").strip():
                self.stderr.write(self.style.WARNING(f"Empty text, skipping: {f}"))
                continue

            # Step 2: Prepare metadata
            title = (f.stem.replace("_", " ").strip()) or f.name
            base_slug = slugify(title)[:512]

            # Slug collision policy (B):
            # Try base slug; on collision with a different file, append deterministic short hash of normalized source path
            norm_src = _normalize_for_hash(str(f))
            target_doc = Document.objects.filter(slug=base_slug).first()
            chosen_slug = base_slug

            if target_doc is None:
                # First occurrence: base slug is fine
                pass
            else:
                # If same slug points to a different file, append hash for uniqueness
                if _normalize_for_hash(target_doc.source_path or "") != norm_src:
                    hashed = _short_hash(norm_src)
                    chosen_slug = f"{base_slug}-{hashed}"
                    target_doc = Document.objects.filter(slug=chosen_slug).first()

            # Step 3: Dry-run mode — no DB writes, just preview actions
            if dry:
                self.stdout.write(
                    f"[dry-run] {f} -> title='{title}', slug='{chosen_slug}', doc_type='{doc_type}'"
                )
                # Preview chunk count
                chunks_preview = sentence_chunks(text, max_chars=max_chars, overlap_chars=overlap)
                self.stdout.write(f"[dry-run] Would create sections: {len(chunks_preview)}")
                continue

            # Step 4: Chunk the text for embedding
            chunks = sentence_chunks(text, max_chars=max_chars, overlap_chars=overlap)
            if not chunks:
                self.stderr.write(self.style.WARNING(f"No chunks produced, skipping: {f}"))
                continue

            # Step 5: Generate embeddings for each chunk
            vecs = embed_texts(chunks)

            # Step 6: Per-file atomic transaction for safe ingestion
            with transaction.atomic():
                created_now = False
                if target_doc is None:
                    # Create new Document entry
                    target_doc = Document.objects.create(
                        title=title,
                        slug=chosen_slug,
                        doc_type=doc_type,
                        source_path=str(f),
                    )
                    created_now = True
                else:
                    # Update doc_type/source_path if changed
                    update = False
                    if target_doc.doc_type != doc_type:
                        target_doc.doc_type = doc_type
                        update = True
                    if _normalize_for_hash(target_doc.source_path or "") != norm_src:
                        target_doc.source_path = str(f)
                        update = True
                    if update:
                        target_doc.save()

                    # Replace mode: clear old sections (and cascaded embeddings) before re-ingesting
                    if not replace:
                        self.stdout.write(self.style.WARNING(
                            f"Document exists and --replace not set, skipping sections: {target_doc.title}"
                        ))
                        continue
                    Section.objects.filter(document=target_doc).delete()

                # Step 7: Bulk insert sections for efficiency
                Section.objects.bulk_create(
                    Section(document=target_doc, index=i, text=ch)
                    for i, ch in enumerate(chunks)
                )

                # Retrieve sections back in index order
                created_sections = list(
                    Section.objects.filter(document=target_doc).order_by("index")
                )

                # Step 8: Bulk insert embeddings linked to sections
                Embedding.objects.bulk_create(
                    Embedding(section=s, model=MODEL_NAME, vector=v.tobytes(), dim=int(v.shape[0]))
                    for s, v in zip(created_sections, vecs)
                )

            # Step 9: Log result
            tag = "Created" if created_now else "Updated"
            self.stdout.write(self.style.SUCCESS(
                f"{tag} '{target_doc.title}' (slug={target_doc.slug}) — {len(chunks)} section(s) with model={MODEL_NAME}"
            ))
