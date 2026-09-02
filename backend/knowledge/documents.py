from pathlib import Path

from langchain_core.documents import Document

from backend.config import KNOWLEDGE_DIR


def load_medical_documents():
    documents = []

    for file_path in KNOWLEDGE_DIR.glob("*.txt"):
        text = file_path.read_text(encoding="utf-8").strip()

        if not text:
            continue

        documents.append(
            Document(
                page_content=text,
                metadata={
                    "topic": file_path.stem,
                    "source_file": file_path.name,
                },
            )
        )

    return documents