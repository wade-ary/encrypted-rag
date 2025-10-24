
import numpy as np #numpy
from typing import List, Any
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
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
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

    def __init__(self):
        """
        Args:
            embedding_dim (int): Dimensionality of output embeddings.
            seed (int): Random seed for reproducibility.
        """
       

    def encode(self, text_chunks: List[str], batch_size: int = 100) -> List[List[float]]:
        """
        Encodes each text chunk into a numeric vector.

        Args:
            text_chunks (List[str]): List of text chunks.

        Returns:
            List[List[float]]: List of embedding vectors (lists of floats).
        """
        model= "sentence-transformers/all-mpnet-base-v2"
        all_embeddings = []

        
        model = SentenceTransformer(model)
        all_embeddings = model.encode(text_chunks, batch_size=32, show_progress_bar=True, convert_to_numpy=True, pool = None)
  

        return all_embeddings
