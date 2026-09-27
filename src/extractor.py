"""Deterministic extraction of basic document structure.

This module sits between text validation and AI-assisted semantic extraction.
It does not call an LLM; it identifies document metadata and common section
headings in a predictable and testable way.
"""

from dataclasses import dataclass


COMMON_SECTION_HEADINGS = {
    "professional experience",
    "experience",
    "work experience",
    "education",
    "skills",
    "technical skills",
    "certifications",
    "projects",
    "summary",
    "professional summary",
    "profile",
    "languages",
}


@dataclass(frozen=True)
class StructuredDocument:
    """Basic structured representation of an extracted document."""

    document_type: str
    page_count: int
    character_count: int
    sections: list[str]


def _normalize_heading(line: str) -> str:
    """Normalize a line for case-insensitive heading comparison."""
    return " ".join(line.strip().lower().split())


def detect_sections(text: str) -> list[str]:
    """Detect common section headings from extracted document text.

    Only headings explicitly present in COMMON_SECTION_HEADINGS are returned.
    The original capitalization from the document is preserved.
    """
    sections: list[str] = []
    seen: set[str] = set()

    for raw_line in text.splitlines():
        line = raw_line.strip()

        if not line or line.startswith("--- Page "):
            continue

        normalized = _normalize_heading(line)

        if normalized in COMMON_SECTION_HEADINGS and normalized not in seen:
            sections.append(line)
            seen.add(normalized)

    return sections


def infer_document_type(text: str) -> str:
    """Infer a basic document type using deterministic signals."""
    normalized = text.lower()

    resume_signals = (
        "professional experience",
        "work experience",
        "education",
        "technical skills",
        "professional summary",
    )

    if sum(signal in normalized for signal in resume_signals) >= 2:
        return "resume"

    return "unknown"


def extract_structure(text: str) -> StructuredDocument:
    """Convert validated extracted text into a basic structured document.

    Args:
        text: Text returned by the PDF ingestion layer.

    Returns:
        StructuredDocument with document metadata and detected sections.

    Raises:
        ValueError: If text is empty or contains no meaningful content.
    """
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Document text cannot be empty.")

    normalized_text = text.strip()

    return StructuredDocument(
        document_type=infer_document_type(normalized_text),
        page_count=normalized_text.count("--- Page "),
        character_count=len(normalized_text),
        sections=detect_sections(normalized_text),
    )
