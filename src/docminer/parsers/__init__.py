"""Document parsers for extracting raw text from PDF and Word files."""

from .pdf import extract_text as extract_pdf_text
from .docx import extract_text as extract_docx_text

__all__ = ["extract_pdf_text", "extract_docx_text"]
