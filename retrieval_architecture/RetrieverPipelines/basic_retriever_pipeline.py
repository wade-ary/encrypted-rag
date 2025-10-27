import os
from retrieval_architecture.retrieval_interfaces import RetrieverPipeline, VectorIndexRetrieval, MetadataRetrieval
from data_setup.ingestion_interfaces import Encryption
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



class BasicRetrieverPipeline(RetrieverPipeline):
    

    def __init__(self, vector_index_retrieval: VectorIndexRetrieval, metadata_retrieval: MetadataRetrieval, encryption_system: Encryption ):
        self.vector_index_retrieval = vector_index_retrieval
        self.metadata_retrieval = metadata_retrieval
        self.encryption_system = encryption_system
        

    def retrieve(self, query: str, top_k: int = 5, permission: str = "public") -> List[Dict[str, Any]]:
        """Given a text query, returns top-k most relevant chunks + metadata."""

        # Search in the vector index to get FAISS IDs + similarity scores
        faiss_ids, scores = self.vector_index_retrieval.search(query, top_k + 10)

        # Retrieve corresponding encrypted_chunks + metadata
        text_chunks = self.metadata_retrieval.get_by_faiss_ids(faiss_ids, permission, top_k, self.encryption_system)
       

        # Combine each chunk with its matching score
        results = []
        for i, chunk_data in enumerate(text_chunks):
            results.append({
                **chunk_data,              # doc_id, chunk, embedding
                "score": scores[i]         # add the similarity score
            })

        return results

        