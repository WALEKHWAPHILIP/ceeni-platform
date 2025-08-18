from pathlib import Path

def parse_pdf(path: str) -> str:
    """
    Extract text content from a PDF file.

    This function first tries `pypdf` for speed and simplicity.
    If that fails (e.g., due to complex layout, encoding issues, or errors),
    it falls back to `pdfminer.six` which is slower but handles more stubborn PDFs.

    Args:
        path (str): Path to the PDF file.

    Returns:
        str: Extracted text with page content concatenated.
    """
    p = Path(path)

    # Ensure the file exists before attempting to parse
    if not p.exists():
        raise FileNotFoundError(path)

    try:
        # --- Primary approach: use pypdf ---
        from pypdf import PdfReader
        reader = PdfReader(str(p))

        # Some PDFs are flagged as "encrypted" but can still be opened without a password
        if getattr(reader, "is_encrypted", False):
            try:
                reader.decrypt("")  # Attempt a blank password; ignore failures
            except Exception:
                pass

        pages = []
        # Extract text from each page (may return None for image-based PDFs)
        for page in reader.pages:
            pages.append(page.extract_text() or "")

        # Join all pages with newlines
        return "\n".join(pages)

    except Exception:
        # --- Fallback approach: use pdfminer.six ---
        # pdfminer handles more complex PDFs, especially with unusual encodings
        from pdfminer.high_level import extract_text
        return extract_text(str(p)) or ""
