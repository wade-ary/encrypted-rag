from abc import ABC, abstractmethod
from typing import List, Dict, Any, Tuple

# 1. VectorIndex — handles FAISS or other vector search
class VectorIndexRetrieval(ABC):
    @abstractmethod
    def search(self, query_vector: List[float], top_k: int = 5) -> Tuple[List[int], List[float]]:
        """Search for top-k similar vectors and return (FAISS IDs, similarity scores)."""
        pass

    @abstractmethod
    def rebuild(self) -> None:
        """Rebuilds the index from stored embeddings (used after deletions)."""
        pass


# 2. MetadataStore — retrieves chunk & metadata info for given FAISS IDs
class MetadataRetrieval(ABC):
    @abstractmethod
    def get_by_faiss_ids(self, faiss_ids: List[int]) -> List[Dict[str, Any]]:
        """Return chunks and metadata corresponding to given FAISS IDs."""
        pass


# 3. Retriever — orchestrates end-to-end retrieval using index + metadata
class RetrieverPipeline(ABC):
    @abstractmethod
    def retrieve(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Given a text query, returns top-k most relevant chunks + metadata."""
        pass
