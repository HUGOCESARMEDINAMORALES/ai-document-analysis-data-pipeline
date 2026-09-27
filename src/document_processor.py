"""PDF document ingestion and text extraction utilities.

This module is intentionally independent from the AI/LLM layer.
Its responsibility is only to read a PDF and return extracted text.
"""

from pathlib import Path

from pypdf import PdfReader


class DocumentProcessingError(Exception):
    """Raised when a PDF cannot be processed."""


def extract_text_from_pdf(file_path: str | Path) -> str:
    """Extract text from all pages of a PDF.

    Args:
        file_path: Local path to the PDF document.

    Returns:
        The extracted text, with page content separated by blank lines.

    Raises:
        DocumentProcessingError: If the file does not exist, is not a PDF,
            or cannot be read.
    """
    path = Path(file_path)

    if not path.exists():
        raise DocumentProcessingError(f"File not found: {path}")

    if not path.is_file():
        raise DocumentProcessingError(f"Path is not a file: {path}")

    if path.suffix.lower() != ".pdf":
        raise DocumentProcessingError(f"Expected a PDF file: {path}")

    try:
        reader = PdfReader(str(path))
        pages = []

        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            pages.append(f"--- Page {page_number} ---\n{text.strip()}")

        return "\n\n".join(pages).strip()

    except Exception as exc:
        raise DocumentProcessingError(
            f"Unable to process PDF '{path.name}': {exc}"
        ) from exc
