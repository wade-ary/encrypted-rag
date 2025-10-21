import os
from datetime import datetime
from typing import Dict, Any

from data_setup.ingestion_interfaces import DocumentLoader


class TxtLoader(DocumentLoader):
    """
    Concrete implementation of DocumentLoader for plain text (.txt) files.
    Reads and returns text content as-is.
    """

    def load(self, file_path: str) -> str:
        """
        Reads the entire contents of a .txt file.

        Args:
            file_path (str): Path to the text file.

        Returns:
            str: Text content of the file.
        """
        if not file_path.lower().endswith(".txt"):
            raise ValueError("Invalid file type. Expected a .txt file.")

        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        return text.strip()

    def get_metadata(self, file_path: str) -> Dict[str, Any]:
        """
        Retrieves basic file metadata (filename, size, creation date, etc.).

        Args:
            file_path (str): Path to the .txt file.

        Returns:
            dict: Metadata dictionary.
        """
        stat = os.stat(file_path)
        metadata = {
            "filename": os.path.basename(file_path),
            "size_bytes": stat.st_size,
            "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "file_type": "txt"
        }
        return metadata