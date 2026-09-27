"""Deterministic mock AI provider for local pipeline testing."""

from __future__ import annotations

import re

from src.ai_extractor import AIExtraction, ExperienceItem


KNOWN_SKILLS = {
    "python": "Python",
    "sql": "SQL",
    "power bi": "Power BI",
    "aws": "AWS",
    "gcp": "GCP",
    "spark": "Apache Spark",
    "pyspark": "PySpark",
    "oracle": "Oracle",
    "postgresql": "PostgreSQL",
    "mysql": "MySQL",
    "airflow": "Apache Airflow",
    "dbt": "dbt",
    "docker": "Docker",
    "git": "Git",
    "ssrs": "SSRS",
    "ssis": "SSIS",
    "ssas": "SSAS",
    "qlikview": "QlikView",
    "sas": "SAS",
    "hive": "Hive",
    "cloudera": "Cloudera",
}


def _extract_skills(text: str) -> list[str]:
    """Detect known technical skills in the source text."""

    normalized_text = text.lower()

    detected = {
        skill_name
        for keyword, skill_name in KNOWN_SKILLS.items()
        if keyword in normalized_text
    }

    return sorted(detected)


def _extract_section(
    text: str,
    start_heading: str,
    end_headings: list[str],
) -> str:
    """Extract text between a section heading and the next section."""

    lines = text.splitlines()

    start_index = None

    for index, line in enumerate(lines):
        if line.strip().lower() == start_heading.lower():
            start_index = index + 1
            break

    if start_index is None:
        return ""

    end_index = len(lines)

    normalized_endings = {
        heading.lower() for heading in end_headings
    }

    for index in range(start_index, len(lines)):
        if lines[index].strip().lower() in normalized_endings:
            end_index = index
            break

    return "\n".join(lines[start_index:end_index]).strip()


def _extract_experience(text: str) -> list[ExperienceItem]:
    """Extract common experience entries from resume-style text."""

    section = _extract_section(
        text,
        "PROFESSIONAL EXPERIENCE",
        [
            "EDUCATION",
            "SKILLS",
            "TECHNICAL SKILLS",
            "CERTIFICATIONS",
            "PROJECTS",
        ],
    )

    if not section:
        return []

    lines = [line.strip() for line in section.splitlines() if line.strip()]

    experiences: list[ExperienceItem] = []

    period_pattern = re.compile(
        r"\b(?:19|20)\d{2}\b.*?(?:\b(?:19|20)\d{2}\b|Present|Current|Now)\b",
        re.IGNORECASE,
    )

    for line in lines:
        if "|" not in line:
            continue

        match = period_pattern.search(line)

        if not match:
            continue

        period = match.group(0).strip()
        before_period = line[:match.start()].strip()

        parts = [part.strip() for part in before_period.split("|")]

        if len(parts) < 2:
            continue

        role = parts[0]
        company = parts[1]

        experiences.append(
            ExperienceItem(
                company=company,
                role=role,
                period=period,
                responsibilities=[],
            )
        )

    return experiences


def _extract_education(text: str) -> list[str]:
    """Extract lines from the education section."""

    section = _extract_section(
        text,
        "EDUCATION",
        [
            "PROFESSIONAL EXPERIENCE",
            "SKILLS",
            "TECHNICAL SKILLS",
            "CERTIFICATIONS",
            "PROJECTS",
        ],
    )

    if not section:
        return []

    return [
        line.strip()
        for line in section.splitlines()
        if line.strip()
    ]


def extract_semantic_data_mock(text: str) -> AIExtraction:
    """Generate structured document data without using an external AI API."""

    if not isinstance(text, str) or not text.strip():
        raise ValueError("Document text cannot be empty.")

    normalized_text = text.lower()

    document_type = (
        "resume"
        if any(
            marker in normalized_text
            for marker in (
                "professional experience",
                "work experience",
                "education",
                "professional summary",
            )
        )
        else "other"
    )

    pages = [
        int(match)
        for match in re.findall(r"--- Page (\d+) ---", text)
    ]

    skills = _extract_skills(text)
    experience = _extract_experience(text)
    education = _extract_education(text)

    return AIExtraction(
        document_type=document_type,
        title="Structured document extraction",
        summary=(
            "Document processed through the local deterministic "
            "extraction provider for pipeline testing."
        ),
        skills=skills,
        experience=experience,
        education=education,
        source_pages=pages,
    )