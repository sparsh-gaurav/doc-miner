"""Data model for document extraction results."""

from dataclasses import dataclass


@dataclass
class ExtractionResult:
    """Outcome of extracting fields from a document."""

    fields: dict
    doc_type: str
    raw_text: str
    error: str | None = None

    @property
    def ok(self) -> bool:
        """Whether extraction succeeded without error and produced fields."""
        return self.error is None and bool(self.fields)
