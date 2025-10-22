
import numpy as np #numpy
from typing import List, Any
import openai
import faiss
import os
from openai import OpenA
from data_setup.ingestion_interfaces import EmbeddingGenerator

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"),
    project=os.getenv("OPENAI_PROJECT_ID"),
    organization= os.getenv("OPENAI_ORG_ID"))

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

    def encode(self, text_chunks: List[str], batch_size: int = 100) -> List[List[float]]:
        """
        Encodes each text chunk into a numeric vector.

        Args:
            text_chunks (List[str]): List of text chunks.

        Returns:
            List[List[float]]: List of embedding vectors (lists of floats).
        """
        all_embeddings = []

        for i in range(0, len(text_chunks), batch_size):
            batch = text_chunks[i:i + batch_size]
            response = client.embeddings.create(
                input=batch,
                model=model
            )
            batch_embeddings = [d.embedding for d in response.data]
            all_embeddings.extend(batch_embeddings)

        return np.array(all_embeddings)
