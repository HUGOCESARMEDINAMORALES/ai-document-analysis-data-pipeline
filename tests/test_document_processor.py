import unittest
from pathlib import Path

from src.document_processor import extract_text_from_pdf


class TestDocumentProcessor(unittest.TestCase):

    def test_extract_text_from_pdf(self):
        pdf_path = Path(
            "data/sample/Hugo_Medina_CV_IT_Service_Management_EN.pdf"
        )

        text = extract_text_from_pdf(pdf_path)

        self.assertIsInstance(text, str)
        self.assertGreater(len(text), 100)
        self.assertIn("--- Page 1 ---", text)


if __name__ == "__main__":
    unittest.main()