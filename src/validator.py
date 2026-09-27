"""Validation utilities for extracted document text.

This module validates the output of the ingestion layer before
the document is sent to downstream extraction or AI processing.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class ValidationResult:
    """Result of document text validation."""

    is_valid: bool
    character_count: int
    page_count: int
    errors: list[str]


class DocumentValidationError(Exception):
    """Raised when document validation fails unexpectedly."""


def validate_extracted_text(
    text: str,
    *,
    minimum_characters: int = 50,
) -> ValidationResult:
    """Validate extracted PDF text.

    Args:
        text: Text returned by the PDF ingestion layer.
        minimum_characters: Minimum amount of meaningful text required.

    Returns:
        A ValidationResult containing validation status and diagnostics.

    Raises:
        DocumentValidationError: If the input is not a string.
    """
    if not isinstance(text, str):
        raise DocumentValidationError("Extracted document content must be a string.")

    normalized_text = text.strip()
    character_count = len(normalized_text)

    page_count = normalized_text.count("--- Page ")

    errors: list[str] = []

    if not normalized_text:
        errors.append("No text was extracted from the document.")

    if character_count < minimum_characters:
        errors.append(
            f"Extracted text is too short: {character_count} characters "
            f"(minimum {minimum_characters})."
        )

    if page_count == 0 and normalized_text:
        errors.append("No page markers were detected in the extracted text.")

    return ValidationResult(
        is_valid=not errors,
        character_count=character_count,
        page_count=page_count,
        errors=errors,
    )
