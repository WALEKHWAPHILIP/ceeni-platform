import re

def normalize_whitespace(text: str) -> str:
    """
    Normalize line breaks and excessive blank lines in text.

    Steps:
    1. Convert all CRLF (\r\n) and CR (\r) line breaks to LF (\n) for consistency.
    2. Collapse sequences of 3+ newlines into exactly 2 newlines (paragraph separation).
    3. Trim leading and trailing whitespace.

    Args:
        text (str): Input text.

    Returns:
        str: Cleaned and normalized text.
    """
    # Standardize newlines to "\n"
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Reduce 3+ consecutive blank lines to exactly 2
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Remove leading/trailing whitespace
    return text.strip()


def sentence_chunks(text: str, max_chars: int = 1400, overlap_chars: int = 120):
    """
    Split text into overlapping chunks based on sentence boundaries.

    Useful for:
    - Feeding text to embedding or LLM APIs with max token/char limits.
    - Preserving semantic flow by including small overlaps between chunks.

    Args:
        text (str): Input text to be chunked.
        max_chars (int): Maximum characters allowed per chunk.
        overlap_chars (int): Number of characters from the end of one chunk
                             to prepend to the next chunk (for context continuity).

    Returns:
        list[str]: List of text chunks.
    """
    # First normalize whitespace
    text = normalize_whitespace(text)

    # Coarsely split text into sentences based on punctuation + whitespace
    parts = re.split(r"(?<=[.!?])\s+", text)

    chunks, buf = [], ""

    # Build chunks up to max_chars
    for part in parts:
        if len(buf) + len(part) + 1 <= max_chars:
            buf = (buf + " " + part).strip()
        else:
            if buf:
                chunks.append(buf)
            buf = part

    # Add last buffer if it exists
    if buf:
        chunks.append(buf)

    # If overlaps are enabled, prepend last `overlap_chars` of the previous chunk
    if overlap_chars and chunks:
        out, tail = [], ""
        for ch in chunks:
            out.append((tail + ch).strip())
            tail = ch[-overlap_chars:]  # keep tail for next chunk
        return out

    return chunks
