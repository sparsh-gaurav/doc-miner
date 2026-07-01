from dataclasses import dataclass


@dataclass
class ExtractionResult:
    fields: dict
    doc_type: str
    raw_text: str
    error: str | None = None

    @property
    def ok(self) -> bool:
        return self.error is None and bool(self.fields)
