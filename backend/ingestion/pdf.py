from pathlib import Path

import pymupdf

from backend.config import CONFIG


def validate_report_file(file_path: str) -> Path:
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if file_path.suffix.lower() not in CONFIG["supported_file_types"]:
        raise ValueError(f"Unsupported file type: {file_path.suffix}")

    return file_path


def extract_pdf_text(file_path: str) -> dict:
    file_path = validate_report_file(file_path)

    pages = []

    with pymupdf.open(file_path) as pdf:
        for page_number, page in enumerate(pdf, start=1):
            text = page.get_text("text")

            pages.append({
                "page": page_number,
                "text": text.strip()
            })

    full_text = "\n\n".join(
        f"[Page {page['page']}]\n{page['text']}"
        for page in pages
        if page["text"]
    )

    return {
        "filename": file_path.name,
        "pages": len(pages),
        "page_data": pages,
        "full_text": full_text
    }