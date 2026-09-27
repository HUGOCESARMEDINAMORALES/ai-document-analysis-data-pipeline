import unittest

from src.validator import validate_extracted_text


class TestValidator(unittest.TestCase):

    def test_valid_document(self):
        text = (
            "--- Page 1 ---\n"
            "This is a valid document with enough content "
            "to pass the validation rules."
        )

        result = validate_extracted_text(text)

        self.assertTrue(result.is_valid)
        self.assertEqual(result.page_count, 1)
        self.assertGreater(result.character_count, 50)
        self.assertEqual(result.errors, [])

    def test_empty_document(self):
        result = validate_extracted_text("")

        self.assertFalse(result.is_valid)
        self.assertGreater(len(result.errors), 0)


if __name__ == "__main__":
    unittest.main()