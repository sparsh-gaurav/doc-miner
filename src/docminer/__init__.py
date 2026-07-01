"""Extract structured key-value data from PDF and Word documents via Gemini."""

from .extractor import extract
from .models import ExtractionResult

__all__ = ["extract", "ExtractionResult"]
__version__ = "0.1.0"
