import fitz

from app.ocr.models import PDFType


class PDFDetector:

    @staticmethod
    def detect(file_path: str) -> PDFType:

        document = fitz.open(file_path)

        page = document[0]

        text = page.get_text().strip()

        document.close()

        if len(text) > 30:
            return PDFType.DIGITAL

        return PDFType.SCANNED