from pathlib import Path
import docx  # python-docx

def parse_docx(path: str) -> str:
    """
    Extract plain text from a Microsoft Word (.docx) file.

    This function uses the `python-docx` library to read the document and
    returns a newline-separated string of all paragraph texts.

    Args:
        path (str): Path to the .docx file.

    Returns:
        str: Extracted text content with paragraphs separated by newlines.
    """
    p = Path(path)

    # Ensure the file exists before attempting to parse
    if not p.exists():
        raise FileNotFoundError(path)

    # Load the DOCX document into memory
    d = docx.Document(str(p))

    # Extract text from each paragraph, skipping empty ones
    # `para.text` returns only plain text, without style or list formatting
    text_content = "\n".join(para.text for para in d.paragraphs if para.text)

    # Remove leading/trailing whitespace from the final string
    return text_content.strip()
