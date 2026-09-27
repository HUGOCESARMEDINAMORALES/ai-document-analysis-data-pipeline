"""Transformation layer for structured document data."""

from dataclasses import dataclass

from src.ai_extractor import AIExtraction


@dataclass(frozen=True)
class TransformedDocument:
    """Normalized document representation for analytical consumption."""

    document_type: str
    title: str
    summary: str
    skills: list[str]
    experience_count: int
    education_count: int
    source_page_count: int


def transform_document(data: AIExtraction) -> TransformedDocument:
    """Transform AI extraction into an analytical representation.

    Args:
        data: Structured semantic extraction.

    Returns:
        A normalized representation suitable for downstream analytics.
    """

    if not isinstance(data, AIExtraction):
        raise TypeError("Expected an AIExtraction object.")

    return TransformedDocument(
        document_type=data.document_type,
        title=data.title.strip(),
        summary=data.summary.strip(),
        skills=sorted(set(data.skills)),
        experience_count=len(data.experience),
        education_count=len(data.education),
        source_page_count=len(set(data.source_pages)),
    )