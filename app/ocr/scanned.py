import pytesseract
from pdf2image import convert_from_path
from app.ocr.preprocess import ImagePreprocessor


class ScannedExtractor:
    @staticmethod
    def extract(file_path: str) -> str:
        """
        Extract text from scanned PDFs using OCR.

        Workflow:
        1. Convert each PDF page into an image.
        2. Preprocess the image for better OCR accuracy.
        3. Run Tesseract OCR on the processed image.
        4. Combine text from all pages.
        """

        # Convert PDF pages to PIL Images
        pages = convert_from_path(file_path)

        extracted_text = []

        for image in pages:
            # Improve image quality for OCR
            processed_image = ImagePreprocessor.preprocess(image)

            # Extract text using Tesseract
            text = pytesseract.image_to_string(processed_image)

            extracted_text.append(text)

        return "\n".join(extracted_text)