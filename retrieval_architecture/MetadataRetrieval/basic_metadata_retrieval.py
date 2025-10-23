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

class BasicMetadataRetrieval:
    def __init__(self, metadata_path: str):
        self.metadata_path = metadata_path

    def get_by_faiss_ids(self, faiss_ids: List[int]) -> List[Dict[str, Any]]:
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
                    # Include any extra info if available (permissions, source, etc.)
                    
                }

        # Collect results for requested FAISS IDs
        results = []
        for fid in faiss_ids:
            if fid in id_to_chunk:
                results.append(id_to_chunk[fid])

        return results

        