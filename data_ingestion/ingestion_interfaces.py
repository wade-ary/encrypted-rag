from abc import ABC, abstractmethod
from typing import List, Dict, Any


# =========================================================
# 1. Abstract Base Classes (Interfaces)
# =========================================================

class DocumentLoader(ABC):
    """Interface for all document loaders (PDF, DOCX, TXT, etc.)."""
    
    @abstractmethod
    def load(self, file_path: str) -> str:
        """Extracts text from a document."""
        pass

    @abstractmethod
    def get_metadata(self, file_path: str) -> Dict[str, Any]:
        """Returns metadata such as title, author, created_date."""
        pass


class TextPreprocessor(ABC):
    """Interface for preprocessing raw text into cleaned, chunked data."""
    
    @abstractmethod
    def clean(self, text: str) -> str:
        """Cleans unwanted characters, whitespace, etc."""
        pass

    @abstractmethod
    def chunk(self, text: str) -> List[str]:
        """Splits text into manageable chunks for embedding."""
        pass


class EmbeddingGenerator(ABC):
    """Interface for embedding generation using various models."""
    
    @abstractmethod
    def encode(self, text_chunks: List[str]) -> List[List[float]]:
        """Encodes each text chunk into an embedding vector."""
        pass


class StorageManager(ABC):
    """Interface for secure storage and retrieval of documents and embeddings."""
    
    @abstractmethod
    def store(
        self,
        doc_id: str,
        chunks: List[str],
        embeddings: List[List[float]],
        metadata: Dict[str, Any]
    ) -> None:
        """Encrypts and stores text chunks + embeddings."""
        pass

    @abstractmethod
    def retrieve(self, doc_id: str) -> Dict[str, Any]:
        """Fetches stored document data and metadata."""
        pass




# =========================================================
# 2. Facade: DocumentIngestionPipeline
# =========================================================

class DocumentIngestionPipeline:
    """
    Orchestrates the ingestion process by composing all modular components.
    """
    
    def __init__(
        self,
        loader: DocumentLoader,
        preprocessor: TextPreprocessor,
        embedder: EmbeddingGenerator,
        storage: StorageManager,
        metadata_manager: MetadataManager
    ):
        self.loader = loader
        self.preprocessor = preprocessor
        self.embedder = embedder
        self.storage = storage
        self.metadata = metadata_manager

    def ingest(self, file_path: str, sector: str, permission: str) -> str:
        """Runs the full ingestion pipeline end-to-end."""
        pass

    def get_ingested_docs(self) -> List[Dict[str, Any]]:
        """Returns a list of all ingested documents and their metadata."""
        pass
