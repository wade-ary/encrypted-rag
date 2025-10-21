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
    Local implementation of the StorageManager interface for embedding data.
    Handles storage and retrieval of document-level embeddings only.
    """

    def __init__(self, storage_path: str = "local_embeddings.json"):
        """
        Args:
            storage_path (str): Path to the JSON file for storing embeddings.
        """
        self.storage_path = storage_path
        self.embeddings_data = self._load_storage()

    def _load_storage(self) -> Dict[str, Any]:
        """Loads existing embedding storage from disk if present."""
        if os.path.exists(self.storage_path):
            with open(self.storage_path, "r", encoding="utf-8") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return {}
        return {}

    def _save_storage(self) -> None:
        """Persists the current in-memory embeddings dictionary to disk."""
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(self.embeddings_data, f, indent=4)

    def store(
        self,
        doc_id: str,
        chunks: List[str],
        embeddings: List[List[float]],
        metadata: Dict[str, Any]
    ) -> None:
        """
        Stores embeddings for a document (text and metadata are ignored here).

        Args:
            doc_id (str): Unique document identifier.
            chunks (List[str]): Ignored (handled by MetadataManager).
            embeddings (List[List[float]]): List of embedding vectors.
            metadata (Dict[str, Any]): Ignored (handled by MetadataManager).
        """
        self.embeddings_data[doc_id] = {
            "embeddings": embeddings
        }
        self._save_storage()

    def retrieve(self, doc_id: str) -> Dict[str, Any]:
        """
        Retrieves stored embeddings for a given document.

        Args:
            doc_id (str): Unique document identifier.

        Returns:
            dict: Dictionary containing "embeddings" if found, else empty dict.
        """
        return self.embeddings_data.get(doc_id, {})

