import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from src.document_processor import extract_text_from_pdf


def create_test_pdf(path: Path) -> None:
    """Create a minimal PDF containing deterministic test text."""

    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        (
            b"<< /Type /Page /Parent 2 0 R "
            b"/MediaBox [0 0 612 792] "
            b"/Resources << /Font << /F1 5 0 R >> >> "
            b"/Contents 4 0 R >>"
        ),
    ]

    content = (
        b"BT "
        b"/F1 18 Tf "
        b"72 720 Td "
        b"(CI Test Document) Tj "
        b"ET"
    )

    objects.append(
        f"<< /Length {len(content)} >>\n".encode()
        + b"stream\n"
        + content
        + b"\nendstream"
    )

    objects.append(
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"
    )

    pdf = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]

    for object_number, obj in enumerate(objects, start=1):
        offsets.append(len(pdf))

        pdf.extend(
            f"{object_number} 0 obj\n".encode()
        )
        pdf.extend(obj)
        pdf.extend(b"\nendobj\n")

    xref_position = len(pdf)

    pdf.extend(
        f"xref\n0 {len(objects) + 1}\n".encode()
    )
    pdf.extend(b"0000000000 65535 f \n")

    for offset in offsets[1:]:
        pdf.extend(
            f"{offset:010d} 00000 n \n".encode()
        )

    pdf.extend(
        (
            f"trailer\n"
            f"<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
            f"startxref\n"
            f"{xref_position}\n"
            f"%%EOF\n"
        ).encode()
    )

    path.write_bytes(pdf)


class TestDocumentProcessor(unittest.TestCase):

    def test_extract_text_from_pdf(self):
        with TemporaryDirectory() as temp_dir:
            pdf_path = Path(temp_dir) / "sample.pdf"

            create_test_pdf(pdf_path)

            text = extract_text_from_pdf(pdf_path)

            self.assertIsInstance(text, str)
            self.assertIn("--- Page 1 ---", text)
            self.assertIn("CI Test Document", text)


if __name__ == "__main__":
    unittest.main()
