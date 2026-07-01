"""Gemini-backed structured field extraction from document text."""

import json
import re

from google import genai
from google.genai import types

from ..models import ExtractionResult

MODEL = "models/gemini-2.5-flash"

PROMPT = """You are a document intelligence system specialized in financial documents.

Analyze the document text below and return a JSON object with:
1. "_doc_type": classify as one of:
   form_16_part_a | form_16_part_b | salary_slip | rent_receipt |
   bank_statement | investment_proof_80c | capital_gains_statement |
   form_26as | ais_tis | other
2. All key information as flat snake_case key-value pairs

Rules:
- Extract ALL important fields: names, dates, amounts, IDs, addresses, percentages
- Values must be exact text from the document (preserve currency symbols, units)
- For repeated data (e.g. quarterly TDS), use nested objects: {{"q1": "5000", "q2": "5000"}}
- Return ONLY valid JSON — no markdown fences, no explanation

Document text:
{text}"""


def extract_fields(text: str, api_key: str) -> ExtractionResult:
    """Send document text to Gemini and parse the returned JSON into an ExtractionResult."""
    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model=MODEL,
        contents=PROMPT.format(text=text[:50_000]),
        config=types.GenerateContentConfig(
            temperature=0.1,
            response_mime_type="application/json",
        ),
    )

    cleaned = _strip_fences(response.text)
    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError as e:
        return ExtractionResult(
            fields={},
            doc_type="unknown",
            raw_text=text,
            error=f"JSON parse error: {e} | raw: {response.text[:300]}",
        )

    doc_type = data.pop("_doc_type", "unknown")
    return ExtractionResult(fields=data, doc_type=doc_type, raw_text=text)


def _strip_fences(text: str) -> str:
    text = text.strip()
    match = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
    return match.group(1).strip() if match else text
