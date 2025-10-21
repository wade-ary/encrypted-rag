
import numpy as np #numpy
from typing import List, Any

from data_setup.ingestion_interfaces import EmbeddingGenerator


class BasicEmbedder(EmbeddingGenerator):
    """
    Basic implementation of the EmbeddingGenerator interface.
    Generates simple numerical embeddings for text chunks.
    
    Used as a placeholder before integrating real models
    (e.g., MPNet, Specter, PubMedBERT).
    """

    def __init__(self, embedding_dim: int = 384, seed: int = 42):
        """
        Args:
            embedding_dim (int): Dimensionality of output embeddings.
            seed (int): Random seed for reproducibility.
        """
        self.embedding_dim = embedding_dim
        self.rng = np.random.default_rng(seed)

    def encode(self, text_chunks: List[str]) -> List[List[float]]:
        """
        Encodes each text chunk into a numeric vector.

        Args:
            text_chunks (List[str]): List of text chunks.

        Returns:
            List[List[float]]: List of embedding vectors (lists of floats).
        """
        embeddings = []
        for chunk in text_chunks:
            # Dummy embedding: deterministic random vector based on text hash
            hash_val = abs(hash(chunk)) % (10**6)
            self.rng = np.random.default_rng(hash_val)
            vector = self.rng.normal(size=self.embedding_dim).tolist()
            embeddings.append(vector)
        return embeddings
