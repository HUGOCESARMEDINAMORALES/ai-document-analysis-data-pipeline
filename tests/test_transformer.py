import unittest

from src.ai_extractor import AIExtraction, ExperienceItem
from src.transformer import transform_document


class TestTransformer(unittest.TestCase):

    def test_transform_document(self):
        data = AIExtraction(
            document_type="resume",
            title="Test Resume",
            summary="Test summary",
            skills=["Python", "SQL", "Python"],
            experience=[
                ExperienceItem(
                    company="Example Bank",
                    role="Data Engineer",
                    period="2020 - 2024",
                    responsibilities=[],
                )
            ],
            education=["Computer Science"],
            source_pages=[1, 2, 2],
        )

        result = transform_document(data)

        self.assertEqual(result.document_type, "resume")
        self.assertEqual(result.title, "Test Resume")
        self.assertEqual(result.experience_count, 1)
        self.assertEqual(result.education_count, 1)
        self.assertEqual(result.source_page_count, 2)

        self.assertEqual(
            result.skills,
            ["Python", "SQL"],
        )

    def test_invalid_input(self):
        with self.assertRaises(TypeError):
            transform_document("invalid")


if __name__ == "__main__":
    unittest.main()
