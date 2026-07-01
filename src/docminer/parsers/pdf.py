import fitz  # PyMuPDF


def extract_text(path: str) -> str:
    doc = fitz.open(path)
    pages = [page.get_text() for page in doc]
    doc.close()
    text = "\n".join(pages)
    if not text.strip():
        raise ValueError(
            "No text extracted from PDF. File may be a scanned/image-only PDF. "
            "OCR support is not included in this version."
        )
    return text
