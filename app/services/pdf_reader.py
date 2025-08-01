# app/services/pdf_reader.py

"""
PDF Reader Service
------------------
Handles PDF file processing and text extraction using PyMuPDF.
"""

import fitz  # PyMuPDF
from pathlib import Path


class PDFReaderService:
    """
    Service to extract text from a given PDF file path.
    """

    @staticmethod
    def extract_text(pdf_path: Path) -> str:
        """
        Extracts all text from a PDF file.

        Args:
            pdf_path (Path): Path to the PDF file.

        Returns:
            str: Extracted full text.
        """
        if not pdf_path.exists() or not pdf_path.is_file():
            raise FileNotFoundError(f"PDF file not found at: {pdf_path}")

        with fitz.open(pdf_path) as doc:
            return "".join(page.get_text() for page in doc)