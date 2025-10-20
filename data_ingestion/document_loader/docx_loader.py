import os
from datetime import datetime
from typing import Dict, Any
import docx  # python-docx

from data_ingestion.ingestion_interfaces import DocumentLoader


class DocxLoader(DocumentLoader):
    """
    Concrete implementation of DocumentLoader for Microsoft Word (.docx) files.
    Extracts visible text and file metadata.
    """

    def load(self, file_path: str) -> str:
        """
        Extracts text from all paragraphs in a Word document.

        Args:
            file_path (str): Path to the .docx file.

        Returns:
            str: Full extracted text with preserved paragraph spacing.
        """
        if not file_path.lower().endswith(".docx"):
            raise ValueError("Invalid file type. Expected a .docx file.")

        doc = docx.Document(file_path)
        paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]
        text = "\n".join(paragraphs)
        return text.strip()

    def get_metadata(self, file_path: str) -> Dict[str, Any]:
        """
        Retrieves basic file metadata (filename, size, creation date, etc.).

        Args:
            file_path (str): Path to the .docx file.

        Returns:
            dict: Metadata dictionary.
        """
        stat = os.stat(file_path)
        metadata = {
            "filename": os.path.basename(file_path),
            "size_bytes": stat.st_size,
            "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "file_type": "docx"
        }
        return metadata