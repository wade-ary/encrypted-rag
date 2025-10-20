import fitz  # PyMuPDF
import os
from typing import Dict, Any
from datetime import datetime

from data_ingestion.ingestion_interfaces import DocumentLoader


class PDFLoader(DocumentLoader):
    """
    Concrete implementation of DocumentLoader for PDF files.
    Extracts text and metadata using PyMuPDF (fitz).
    """

    def load(self, file_path: str) -> str:
        """
        Extracts all text from the PDF file.

        Args:
            file_path (str): Path to the PDF file.

        Returns:
            str: Full extracted text.
        """
        if not file_path.lower().endswith(".pdf"):
            raise ValueError("Invalid file type. Expected a .pdf file.")

        text = ""
        with fitz.open(file_path) as pdf:
            for page in pdf:
                text += page.get_text("text")

        return text.strip()

    def get_metadata(self, file_path: str) -> Dict[str, Any]:
        """
        Retrieves basic file metadata (filename, size, creation date, etc.).

        Args:
            file_path (str): Path to the PDF file.

        Returns:
            dict: Metadata dictionary.
        """
        stat = os.stat(file_path)
        metadata = {
            "filename": os.path.basename(file_path),
            "size_bytes": stat.st_size,
            "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "file_type": "pdf"
        }
        return metadata