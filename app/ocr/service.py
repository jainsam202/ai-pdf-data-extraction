from app.ocr.cleaner import TextCleaner
from app.ocr.detector import PDFDetector
from app.ocr.digital import DigitalExtractor
from app.ocr.models import PDFType
from app.ocr.scanned import ScannedExtractor


class OCRService:

    @staticmethod
    def extract(file_path: str):

        pdf_type = PDFDetector.detect(file_path)

        if pdf_type == PDFType.DIGITAL:

            text = DigitalExtractor.extract(file_path)

        else:

            text = ScannedExtractor.extract(file_path)

        return TextCleaner.clean(text)