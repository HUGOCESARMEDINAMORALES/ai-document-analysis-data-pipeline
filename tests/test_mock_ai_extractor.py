import unittest

from src.mock_ai_extractor import extract_semantic_data_mock


class TestMockAIExtractor(unittest.TestCase):

    def test_extract_structured_data(self):
        text = """
        PROFESSIONAL SUMMARY
        Data Engineer with experience in Python and SQL.

        PROFESSIONAL EXPERIENCE
        Data Engineer | Example Bank | 2020 - 2024

        EDUCATION
        Bachelor's Degree in Computer Science

        TECHNICAL SKILLS
        Python, SQL, AWS, Spark
        """

        result = extract_semantic_data_mock(text)

        self.assertEqual(result.document_type, "resume")
        self.assertIn("Python", result.skills)
        self.assertIn("SQL", result.skills)
        self.assertEqual(len(result.experience), 1)
        self.assertEqual(len(result.education), 1)

    def test_empty_document(self):
        with self.assertRaises(ValueError):
            extract_semantic_data_mock("")


if __name__ == "__main__":
    unittest.main()