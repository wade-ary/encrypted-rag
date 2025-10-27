
import pytest
import sys, os
sys.path.append(os.path.abspath(os.getcwd()))
from data_setup.ingestion_interfaces import DocumentIngestionPipeline, DocumentLoader, TextPreprocessor, EmbeddingGenerator,StorageManager 
from data_setup.document_loader.pdf_loader import PDFLoader
from data_setup.document_loader.docx_loader import DocxLoader
from data_setup.document_loader.txt_loader import TxtLoader
from data_setup.embedding_generator.basic_embedder import BasicEmbedder
from data_setup.text_preprocessor.basic_preprocessor import BasicPreprocessor
from data_setup.storage_manager.local_storage_manager import LocalStorageManager
from data_setup.encryption_system.basic_encryption import BasicEncryption
import os
import sys, os
SAMPLE_DIR = "/Users/aryamanwade/Desktop/encrypt_rag/encrypted-rag/test/sample_text"
from sentence_transformers import SentenceTransformer



class BasicIngestionPipeline(DocumentIngestionPipeline):
    """
    Basic implementation of the ingestion pipeline that:
    1. Loads a document using a generic DocumentLoader (PDF, DOCX, TXT, etc.)
    2. Preprocesses text into smaller chunks
    3. Generates embeddings for each chunk
    4. Stores them in FAISS + metadata store
    """

    def __init__(
        self,
        loader: DocumentLoader,
        preprocessor: TextPreprocessor,
        embedder: EmbeddingGenerator,
        storage: StorageManager,
        encryption: BasicEncryption,
  
    ):
        self.loader = loader
        self.preprocessor = preprocessor
        self.embedder = embedder
        self.storage = storage
        self.encryption = encryption
 
    def ingest(self, file_path: str, permission: str) -> None:
        """Runs the full ingestion pipeline end-to-end."""
        
        # Load document 
        full_path = os.path.join(SAMPLE_DIR, file_path)
        text = self.loader.load(full_path)
        metadata = self.loader.get_metadata(full_path)
        metadata.update({"permission": permission})

        # Preprocess text into chunks 
        chunks = self.preprocessor.chunk(text)
        chunks_encrypted = []
        for chunk in chunks:
            chunks_encrypted.append(self.encryption.encrypt(chunk, permission))
            
        # Generate embeddings for all chunks 
        embeddings = self.embedder.encode(chunks)

        # Store document, chunks, embeddings, and metadata
        doc_id = os.path.splitext(os.path.basename(file_path))[0]
        self.storage.store(doc_id, chunks_encrypted, embeddings, metadata)

        # For now, returns None (can later return doc_id or summary)
        return None
        
        