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
import faiss 
import numpy as np

from data_setup.ingestion_interfaces import StorageManager


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
        Adds embeddings for a document into the FAISS index while maintaining
        a mapping of which vector IDs belong to which document.

        Args:
            doc_id (str): Unique document identifier.
            chunks (List[str]): Ignored (handled by MetadataManager).
            embeddings (List[List[float]]): List of embedding vectors.
            metadata (Dict[str, Any]): Ignored (handled by MetadataManager).
        """
    
    
        base_dir = "data_store"
        index_path = "/Users/aryamanwade/Desktop/encrypt_rag/encrypted-rag/data_store/faiss_index.bin"
        mapping_path = "/Users/aryamanwade/Desktop/encrypt_rag/encrypted-rag/data_store/embedding_map.json"

        os.makedirs(base_dir, exist_ok=True)

        # Convert embeddings to NumPy array and normalize
        embedding_array = np.array(embeddings).astype("float32")
        faiss.normalize_L2(embedding_array)

        # Load or initialize index
        if os.path.exists(index_path):
            index = faiss.read_index(index_path)
        else:
            dim = embedding_array.shape[1]
            index = faiss.IndexFlatIP(dim)

        # Record start and end IDs for this document
        start_id = index.ntotal
        index.add(embedding_array)
        end_id = index.ntotal
        new_ids = list(range(start_id, end_id))

        # Update mapping (FAISS ID → doc reference)
        if os.path.exists(mapping_path):
            with open(mapping_path, "r", encoding="utf-8") as f:
                try:
                    id_map = json.load(f)
                except json.JSONDecodeError:
                    id_map = {}
        else:
            id_map = {}

        # --- Update document entry ---
        id_map[doc_id] = {
            "faiss_ids": new_ids,          # FAISS vector IDs for this document
            "chunks": chunks,              # raw text chunks
            "embeddings": embeddings.tolist(),      # store embeddings for rebuilds
            "metadata": metadata,          # extra info like filename, path, etc.
            "count": len(new_ids)
        }

        # --- Save metadata + FAISS index ---
        with open(mapping_path, "w", encoding="utf-8") as f:
            json.dump(id_map, f, indent=4)

        faiss.write_index(index, index_path)


    def retrieve(self, doc_id: str) -> Dict[str, Any]:
        """
        Retrieves stored embeddings for a given document.

        Args:
            doc_id (str): Unique document identifier.

        Returns:
            dict: Dictionary containing "embeddings" if found, else empty dict.
        """
        return self.embeddings_data.get(doc_id, {})

