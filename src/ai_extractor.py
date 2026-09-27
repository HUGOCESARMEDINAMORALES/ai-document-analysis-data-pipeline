"""AI-assisted semantic extraction using OpenAI Structured Outputs.

The module receives validated text from the deterministic pipeline and asks
an LLM to map semantic information into a typed Pydantic model.

Secrets are loaded from environment variables; no API key is hard-coded.
"""

from __future__ import annotations

import os
from typing import Literal

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field


load_dotenv()


class ExperienceItem(BaseModel):
    """A normalized professional experience entry."""

    company: str = Field(description="Organization or employer name, if present.")
    role: str = Field(description="Job title or role, if present.")
    period: str = Field(description="Employment period exactly as supported by the source.")
    responsibilities: list[str] = Field(
        description="Key responsibilities explicitly supported by the document."
    )


class AIExtraction(BaseModel):
    """Structured semantic information extracted from a document."""

    document_type: Literal["resume", "report", "invoice", "contract", "other"]
    title: str
    summary: str
    skills: list[str]
    experience: list[ExperienceItem]
    education: list[str]
    source_pages: list[int]


class AIExtractionError(Exception):
    """Raised when AI-assisted extraction cannot be completed."""


def _get_client() -> OpenAI:
    """Create an OpenAI client using the environment configuration."""
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise AIExtractionError(
            "OPENAI_API_KEY is not configured. Add it to the local environment "
            "before running AI-assisted extraction."
        )

    return OpenAI(api_key=api_key)


def extract_semantic_data(
    text: str,
    *,
    model: str | None = None,
) -> AIExtraction:
    """Extract semantic information from validated document text.

    The request uses the Responses API with Structured Outputs so the model
    response conforms to the AIExtraction Pydantic schema.
    """
    if not isinstance(text, str) or not text.strip():
        raise AIExtractionError("Document text cannot be empty.")

    client = _get_client()
    selected_model = model or os.getenv("OPENAI_MODEL", "gpt-5.6-luna")

    instructions = (
        "Extract only information supported by the source document. "
        "Do not invent missing facts. Preserve dates and role names as written. "
        "Return empty strings or empty lists when information is unavailable. "
        "For source_pages, include the page numbers where the extracted "
        "information appears. Classify the document as resume, report, invoice, "
        "contract, or other."
    )

    try:
        response = client.responses.parse(
            model=selected_model,
            input=[
                {
                    "role": "system",
                    "content": instructions,
                },
                {
                    "role": "user",
                    "content": text,
                },
            ],
            text_format=AIExtraction,
            store=False,
        )

        if response.output_parsed is None:
            raise AIExtractionError(
                "The model returned no structured extraction."
            )

        return response.output_parsed

    except AIExtractionError:
        raise
    except Exception as exc:
        raise AIExtractionError(
            f"AI-assisted extraction failed: {exc}"
        ) from exc
