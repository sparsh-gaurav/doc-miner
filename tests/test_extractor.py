import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path

from docextract import extract, ExtractionResult


MOCK_FIELDS = {
    "employee_name": "Sparsh Gaurav",
    "gross_salary": "₹12,00,000",
    "tds_deducted": "₹1,20,000",
    "pan": "ABCDE1234F",
}

MOCK_RESULT = ExtractionResult(
    fields=MOCK_FIELDS,
    doc_type="form_16_part_b",
    raw_text="dummy text",
)


def test_extract_pdf_success(tmp_path):
    dummy_pdf = tmp_path / "form16.pdf"
    dummy_pdf.write_bytes(b"%PDF-1.4 dummy")

    with (
        patch("docextract.extractor._pdf_text", return_value="extracted text"),
        patch("docextract.extractor._gemini_extract", return_value=MOCK_RESULT),
    ):
        result = extract(dummy_pdf, api_key="test-key")

    assert result.ok
    assert result.doc_type == "form_16_part_b"
    assert result.fields["employee_name"] == "Sparsh Gaurav"


def test_extract_docx_success(tmp_path):
    dummy_docx = tmp_path / "salary.docx"
    dummy_docx.write_bytes(b"PK dummy docx")

    with (
        patch("docextract.extractor._docx_text", return_value="extracted text"),
        patch("docextract.extractor._gemini_extract", return_value=MOCK_RESULT),
    ):
        result = extract(dummy_docx, api_key="test-key")

    assert result.ok


def test_extract_missing_file():
    with pytest.raises(FileNotFoundError):
        extract("/nonexistent/path/file.pdf", api_key="test-key")


def test_extract_unsupported_extension(tmp_path):
    f = tmp_path / "doc.txt"
    f.write_text("hello")
    with pytest.raises(ValueError, match="Unsupported file type"):
        extract(f, api_key="test-key")


def test_extract_no_api_key(tmp_path, monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    f = tmp_path / "file.pdf"
    f.write_bytes(b"%PDF")
    with pytest.raises(EnvironmentError, match="Gemini API key"):
        extract(f)


def test_extraction_result_ok_false_on_error():
    result = ExtractionResult(fields={}, doc_type="unknown", raw_text="", error="failed")
    assert not result.ok


def test_extraction_result_ok_false_on_empty_fields():
    result = ExtractionResult(fields={}, doc_type="form_16_part_b", raw_text="text")
    assert not result.ok
