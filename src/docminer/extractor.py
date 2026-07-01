"""Top-level document extraction entry point."""

import os
from pathlib import Path

from .models import ExtractionResult
from .parsers.pdf import extract_text as _pdf_text
from .parsers.docx import extract_text as _docx_text
from .llm.gemini import extract_fields as _gemini_extract

_SUPPORTED = {".pdf", ".docx", ".doc"}


def extract(source: str | Path, api_key: str | None = None) -> ExtractionResult:
    """Extract key-value pairs from a PDF or Word document.

    Args:
        source: Path to a .pdf, .docx, or .doc file.
        api_key: Gemini API key. Falls back to GEMINI_API_KEY env var.

    Returns:
        ExtractionResult with .fields dict, .doc_type string, and .ok bool.

    Raises:
        FileNotFoundError: File does not exist.
        ValueError: Unsupported file type or no text could be extracted.
        EnvironmentError: No API key provided or found in environment.
    """
    api_key = api_key or os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "Gemini API key required. Pass api_key= or set GEMINI_API_KEY env var."
        )

    path = Path(source)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    suffix = path.suffix.lower()
    if suffix not in _SUPPORTED:
        raise ValueError(f"Unsupported file type '{suffix}'. Supported: {_SUPPORTED}")

    if suffix == ".pdf":
        text = _pdf_text(str(path))
    else:
        text = _docx_text(str(path))

    return _gemini_extract(text, api_key)
