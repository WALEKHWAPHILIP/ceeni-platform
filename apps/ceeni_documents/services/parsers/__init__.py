"""
Parser package initialization.

This module re-exports the main file parsing functions so they can be
imported directly from the package without referencing submodules.

Example:
    Instead of:
        from parsers.pdf_parser import parse_pdf
        from parsers.docx_parser import parse_docx
        from parsers.html_parser import parse_html

    You can now do:
        from parsers import parse_pdf, parse_docx, parse_html
"""

from .pdf_parser import parse_pdf
from .docx_parser import parse_docx
from .html_parser import parse_html

# Define the public API for this package
__all__ = [
    "parse_pdf",
    "parse_docx",
    "parse_html",
]
