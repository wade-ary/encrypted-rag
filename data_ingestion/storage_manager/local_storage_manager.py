# ==========================
# 📦 Dependencies
# ==========================
# json
# os
# typing
# ==========================

import os
import json
from typing import List, Dict, Any

from data_ingestion.ingestion_interfaces import StorageManager


class LocalStorageManager(StorageManager):
    """
    Basic local implementation of the StorageManager interface.
    Stores text chunks and metadata in a JSON file (no FAISS yet).
    """

    def __init__(self, storage_path: str = "local_storage.json"):
        """
        Args:
            storage_path (str): Path to the JSON file for storing data.
        """
        self.storage_path = storage_path
        self.data = self._load_storage()

    def _load_storage(self) -> Dict[str, Any]:
        """Loads existing storage from disk if present."""
        if os.path.exists(self.storage_path):
            with open(self.storage_path, "r", encoding="utf-8") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return {}
        return {}

    def _save_storage(self) -> None:
        """Persists the current in-memory data dictionary to disk."""
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4)

    def store(
        self,
        doc_id: str,
        chunks: List[str],
        embeddings: List[List[float]],
        metadata: Dict[str, Any]
    ) -> None:
        """
        Stores chunks and metadata locally under the given doc_id.

        Args:
            doc_id (str): Unique document identifier.
            chunks (List[str]): Text chunks from the document.
            embeddings (List[List[float]]): Embedding vectors (placeholder).
            metadata (Dict[str, Any]): Document-level metadata.
        """
        self.data[doc_id] = {
            "chunks": chunks,
            "metadata": metadata
        }
        self._save_storage()

    def retrieve(self, doc_id: str) -> Dict[str, Any]:
        """
        Fetches stored document data and metadata.

        Args:
            doc_id (str): Unique document identifier.

        Returns:
            dict: Dictionary containing "chunks" and "metadata".
        """
        return self.data.get(doc_id, {})
