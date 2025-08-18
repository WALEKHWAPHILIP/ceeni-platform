from pathlib import Path
from bs4 import BeautifulSoup

def parse_html(path_or_html: str, *, is_html: bool = False) -> str:
    """
    Extract visible text content from an HTML document or HTML string.

    This function removes non-visible elements such as <script>, <style>, and
    <noscript> tags before returning the cleaned, readable text.

    Args:
        path_or_html (str):
            - If `is_html` is False (default), this is treated as a file path to an HTML file.
            - If `is_html` is True, this is treated as a raw HTML string.
        is_html (bool): Whether `path_or_html` is already HTML markup.

    Returns:
        str: Extracted visible text with newline separation.
    """
    # Load HTML content from a string or a file path
    if is_html:
        html = path_or_html
    else:
        html = Path(path_or_html).read_text(encoding="utf-8", errors="ignore")

    # Parse HTML content into a DOM-like tree
    soup = BeautifulSoup(html, "html.parser")

    # Remove tags that contain non-visible or non-textual content
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    # Extract only the visible text content, separated by newlines
    # This strips all HTML tags and flattens structure into plain text
    return soup.get_text("\n").strip()
