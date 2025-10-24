import os
from retrieval_architecture.retrieval_interfaces import VectorIndexRetrieval
import numpy as np #numpy
from typing import List, Tuple, Any
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


class BasicVectorRetrieval:
    def __init__(self, index_path: str, model_name: str = "sentence-transformers/all-mpnet-base-v2"):
        self.index_path = index_path
        self.model = SentenceTransformer(model_name)

    def search(self, query: str, top_k: int = 5) -> Tuple[List[int], List[float]]:
        """Search for top-k similar vectors and return (FAISS IDs, similarity scores)."""

        # Encode the query into a vector
        query_embedding = self.model.encode([query], convert_to_numpy=True, normalize_embeddings=True)
        # shape = (1, embedding_dim)

        # Load the FAISS index
        index = faiss.read_index(self.index_path)

        # Perform the similarity search
        D, I = index.search(query_embedding, top_k)
        # D: distances or similarity scores, shape (1, top_k)
        # I: FAISS IDs, shape (1, top_k)

        # Return as lists
        return I[0].tolist(), D[0].tolist()