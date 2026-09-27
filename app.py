"""Streamlit application for the document analysis pipeline."""

import streamlit as st

from src.document_processor import extract_text_from_pdf
from src.mock_ai_extractor import extract_semantic_data_mock
from src.transformer import transform_document
from src.validator import validate_extracted_text


st.set_page_config(
    page_title="AI Document Analysis Pipeline",
    page_icon="📄",
    layout="wide",
)

st.title("📄 AI-Powered Document Analysis")
st.caption(
    "End-to-end document ingestion, validation, structured extraction, "
    "and analytical transformation."
)

uploaded_file = st.file_uploader(
    "Upload a PDF document",
    type=["pdf"],
)

if uploaded_file is not None:
    try:
        with st.spinner("Processing document..."):
            temp_path = "/tmp/uploaded_document.pdf"

            with open(temp_path, "wb") as file:
                file.write(uploaded_file.getbuffer())

            # 1. Document ingestion
            text = extract_text_from_pdf(temp_path)

            # 2. Validation
            validation = validate_extracted_text(text)

            if not validation.is_valid:
                st.error("Document validation failed.")

                for error in validation.errors:
                    st.write(f"- {error}")

                st.stop()

            # 3. Semantic extraction
            ai_result = extract_semantic_data_mock(text)

            # 4. Transformation
            transformed = transform_document(ai_result)

        st.success("Document processed successfully.")

        # ---------------------------------------------------------
        # Metrics
        # ---------------------------------------------------------

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Characters",
                validation.character_count,
            )

        with col2:
            st.metric(
                "Pages",
                validation.page_count,
            )

        with col3:
            st.metric(
                "Skills",
                len(transformed.skills),
            )

        with col4:
            st.metric(
                "Experience",
                transformed.experience_count,
            )

        # ---------------------------------------------------------
        # Summary
        # ---------------------------------------------------------

        st.subheader("📋 Document Summary")

        st.write(transformed.summary)

        # ---------------------------------------------------------
        # Skills
        # ---------------------------------------------------------

        st.subheader("🛠️ Detected Skills")

        if transformed.skills:
            for skill in transformed.skills:
                st.write(f"- {skill}")
        else:
            st.info("No supported skills detected.")

        # ---------------------------------------------------------
        # Experience
        # ---------------------------------------------------------

        st.subheader("💼 Professional Experience")

        if ai_result.experience:
            for experience in ai_result.experience:
                st.markdown(
                    f"**{experience.role}** — {experience.company}"
                )
                st.write(f"Period: {experience.period}")
        else:
            st.info("No professional experience detected.")

        # ---------------------------------------------------------
        # Education
        # ---------------------------------------------------------

        st.subheader("🎓 Education")

        if ai_result.education:
            for education in ai_result.education:
                st.write(f"- {education}")
        else:
            st.info("No education information detected.")

        # ---------------------------------------------------------
        # Source pages
        # ---------------------------------------------------------

        st.subheader("📄 Source Pages")

        if ai_result.source_pages:
            st.write(
                f"Information was extracted from pages: "
                f"{', '.join(map(str, ai_result.source_pages))}"
            )
        else:
            st.info("No source page information available.")

        # ---------------------------------------------------------
        # Structured output
        # ---------------------------------------------------------

        st.subheader("🔎 Structured Output")

        st.json(
            {
                "document_type": transformed.document_type,
                "title": transformed.title,
                "summary": transformed.summary,
                "skills": transformed.skills,
                "experience_count": transformed.experience_count,
                "education_count": transformed.education_count,
                "source_page_count": transformed.source_page_count,
            }
        )

    except Exception as exc:
        st.error(
            f"An error occurred while processing the document: {exc}"
        )