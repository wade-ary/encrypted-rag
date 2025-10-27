import os
from retrieval_architecture.retrieval_interfaces import MetadataRetrieval
import numpy as np #numpy
from typing import Dict, List, Any
import openai
import faiss
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"
from sentence_transformers import SentenceTransformer
import json
from data_setup.encryption_system.basic_encryption import BasicEncryption

class BasicMetadataRetrieval:
    def __init__(self, metadata_path: str):
        self.metadata_path = metadata_path

    def get_by_faiss_ids(self, faiss_ids: List[int], permission: str, top_k: int, encryption) -> List[Dict[str, Any]]:
        """Return chunks and metadata corresponding to given FAISS IDs."""
        
        # Load the metadata JSON
        with open(self.metadata_path, "r") as f:
            metadata = json.load(f)

        # Flatten all documents' FAISS data into a lookup map
        id_to_chunk = {}
        for doc_id, doc_data in metadata.items():
            for idx, faiss_id in enumerate(doc_data["faiss_ids"]):
                id_to_chunk[faiss_id] = {
                    "doc_id": doc_id,
                    "chunk": doc_data["chunks"][idx],
                    "embedding": doc_data["embeddings"][idx],
                    "permission": doc_data.get("metadata", {}).get("permission", "public")
                    
                    
                }

        hierarchy = {"public": 1, "employee": 2, "admin": 3}
        user_level = hierarchy.get(permission, 1)

        # Retrieve a few extra
        faiss_ids_extended = faiss_ids[:top_k + 10]
       
        results = []
        for fid in faiss_ids_extended:
            if fid in id_to_chunk:
                doc = id_to_chunk[fid]
                doc_level = hierarchy.get(doc["permission"], 1)

                # Keep only if user's level >= doc's level
                if user_level >= doc_level:
                    # 🔓 Decrypt the chunk using the document’s permission level
                    encrypted_text = doc["chunk"]
                    decrypted_text = encryption.decrypt(encrypted_text, doc["permission"])
                    doc["chunk"] = decrypted_text  # replace ciphertext with plaintext
                    results.append(doc)

            # Stop once we have enough
            if len(results) >= top_k:
                break

        return results

        