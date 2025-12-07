# src/utils/document_loader.py
import os
from pathlib import Path
from typing import Any, Dict

from pypdf import PdfReader

from models.types import Document


def load_pdf_as_text(path: str) -> tuple[str, Dict[str, Any]]:
    reader = PdfReader(path)
    text_chunks = []
    for page in reader.pages:
        text_chunks.append(page.extract_text() or "")

    full_text = "\n\n".join(text_chunks)

    # PDF metadata (may be None or incomplete)
    meta = reader.metadata or {}
    title = meta.title if getattr(meta, "title", None) else Path(path).stem

    metadata: Dict[str, Any] = {
        "title": title,
        "source_path": os.path.abspath(path),
        "file_name": Path(path).name,
        "file_type": "pdf",
        "page_count": len(reader.pages),
        "pdf_metadata": {
            "author": getattr(meta, "author", None),
            "subject": getattr(meta, "subject", None),
        },
    }

    return full_text, metadata


def load_txt_as_text(path: str) -> tuple[str, Dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    metadata: Dict[str, Any] = {
        "title": Path(path).stem,
        "source_path": os.path.abspath(path),
        "file_name": Path(path).name,
        "file_type": "txt",
    }

    return content, metadata


def load_document(path: str) -> Document:
    ext = Path(path).suffix.lower()

    if ext == ".pdf":
        content, metadata = load_pdf_as_text(path)
    elif ext in {".txt", ".md"}:
        content, metadata = load_txt_as_text(path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

    # Document id derived from filename (stable, human-readable)
    doc_id = Path(path).stem

    return Document(
        id=doc_id,
        content=content,
        metadata=metadata,
    )
