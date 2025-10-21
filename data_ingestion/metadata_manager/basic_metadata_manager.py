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

from data_ingestion.ingestion_interfaces import MetadataManager


class BasicMetadataManager(MetadataManager):
    """
    Local implementation of MetadataManager for storing document metadata and raw text chunks.
    Handles sector, permission, and metadata tracking for all ingested documents.
    """

    def __init__(self, storage_path: str = "local_metadata.json"):
        """
        Args:
            storage_path (str): Path to the JSON file for storing metadata and chunks.
        """
        self.storage_path = storage_path
        self.metadata_store = self._load_storage()

    def _load_storage(self) -> Dict[str, Any]:
        """Loads existing metadata storage from disk if present."""
        if os.path.exists(self.storage_path):
            with open(self.storage_path, "r", encoding="utf-8") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return {}
        return {}

    def _save_storage(self) -> None:
        """Persists the current in-memory metadata dictionary to disk."""
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(self.metadata_store, f, indent=4)

    def register(
        self,
        doc_id: str,
        sector: str,
        permission: str,
        metadata: Dict[str, Any],
        chunks: List[str]
    ) -> None:
        """
        Registers document metadata and stores raw text chunks.

        Args:
            doc_id (str): Unique document identifier.
            sector (str): Sector label (used for access control).
            permission (str): Access level (e.g., 'confidential', 'restricted').
            metadata (Dict[str, Any]): Additional metadata (filename, timestamps, etc.).
            chunks (List[str]): Cleaned text chunks from the document.
        """
        self.metadata_store[doc_id] = {
            "sector": sector,
            "permission": permission,
            "metadata": metadata,
            "chunks": chunks
        }
        self._save_storage()

    def list_documents(self, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Lists registered documents, optionally filtered by sector or permission.

        Args:
            filters (Dict[str, Any], optional): Filter keys such as {'sector': 'intel'}.

        Returns:
            List[Dict[str, Any]]: List of matching documents with metadata.
        """
        results = []
        for doc_id, info in self.metadata_store.items():
            if filters:
                if any(info.get(k) != v for k, v in filters.items()):
                    continue
            results.append({"doc_id": doc_id, **info})
        return results
