# docextract

Extract structured key-value data from any PDF or Word document using a free LLM.

No templates. No rules. Drop in a document — get back a clean JSON of everything important.

```python
from docextract import extract

result = extract("invoice.pdf")
print(result.doc_type)  # "invoice"
print(result.fields)    # {"vendor": "Acme Ltd", "total": "$1,200", "due_date": "2026-08-01", ...}
```

## How it works

1. Extracts raw text from the file (PDF or Word)
2. Sends the text to **Gemini 2.0 Flash** with a prompt to identify and return all key fields
3. Returns a structured dict — no schema needed, the LLM decides what matters

## Supported File Types

- `.pdf` — text-based PDFs (not scanned/image-only)
- `.docx` / `.doc` — Word documents including tables

## Getting a Free Gemini API Key

1. Go to [aistudio.google.com](https://aistudio.google.com)
2. Sign in with a Google account
3. Click **"Get API key"** → **"Create API key"**
4. Copy the key — no credit card required

**Free tier limits:** 1,500 requests/day · 1M tokens/min

## Installation

```bash
git clone https://github.com/your-username/docextract.git
cd docextract

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -e ".[dev]"
```

## Configuration

```bash
cp .env.example .env
# add your key:
# GEMINI_API_KEY=your_key_here
```

Or pass the key directly in code:

```python
result = extract("document.pdf", api_key="your_key_here")
```

## Usage

```python
from docextract import extract

result = extract("contract.pdf")

if result.ok:
    print(result.doc_type)   # auto-detected document type
    print(result.fields)     # all extracted key-value pairs
else:
    print(result.error)
```

### ExtractionResult fields

| Field | Type | Description |
|---|---|---|
| `fields` | `dict` | Extracted key-value pairs |
| `doc_type` | `str` | Auto-detected document type |
| `raw_text` | `str` | Raw text parsed from the file |
| `ok` | `bool` | `True` if extraction succeeded |
| `error` | `str \| None` | Error message if extraction failed |

## Running Tests

```bash
source .venv/bin/activate
pytest tests/ -v
```

## Project Structure

```
docextract/
├── src/docextract/
│   ├── extractor.py        # main extract() function
│   ├── models.py           # ExtractionResult dataclass
│   ├── parsers/
│   │   ├── pdf.py          # PDF text extraction via PyMuPDF
│   │   └── docx.py         # Word extraction via python-docx
│   └── llm/
│       └── gemini.py       # Gemini 2.0 Flash client
└── tests/
    └── test_extractor.py
```

## Limitations

- Scanned / image-only PDFs are not supported — the file must contain selectable text
- Documents are truncated to 50,000 characters before being sent to the LLM

## Roadmap

- [ ] OCR support for scanned PDFs
- [ ] Batch extraction for multiple files
- [ ] Schema-driven mode (specify which fields to extract)
- [ ] Support for additional LLM providers

## License

MIT
