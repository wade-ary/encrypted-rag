import pytest
import sys, os
sys.path.append(os.path.abspath(os.getcwd()))
from data_setup.document_loader.pdf_loader import PDFLoader
from data_setup.document_loader.docx_loader import DocxLoader
from data_setup.document_loader.txt_loader import TxtLoader
from data_setup.embedding_generator.basic_embedder import BasicEmbedder
from data_setup.text_preprocessor.basic_preprocessor import BasicPreprocessor
from data_setup.storage_manager.local_storage_manager import LocalStorageManager
from data_setup.encryption_system.basic_encryption import BasicEncryption
from data_setup.encryption_system.aes_encryption import AESEncryption
from data_setup.document_ingestion_pipeline.basic_ingestion_pipeline import BasicIngestionPipeline
import os
import sys, os
SAMPLE_DIR = "/Users/aryamanwade/Desktop/encrypt_rag/encrypted-rag/test/sample_text"
from sentence_transformers import SentenceTransformer
import inspect


loader = PDFLoader()

preprocess = BasicPreprocessor()
embedder = BasicEmbedder()
encryption = AESEncryption()
data_store = LocalStorageManager()

ingestion_pipeline = BasicIngestionPipeline(loader,preprocess, embedder, data_store, encryption)
file_path1 = os.path.join(SAMPLE_DIR, "fullarticle_2024-0010.pdf")
file_path2 = os.path.join(SAMPLE_DIR, "96648955-en.pdf")
file_path3 = os.path.join(SAMPLE_DIR, "commentary351e.pdf")
file_path4 = os.path.join(SAMPLE_DIR, "Japans-Forgotten-Countryside-Demographic-Crisis-and-Revival-Strategies.pdf")
file_path5 = os.path.join(SAMPLE_DIR, "ko250824a1.pdf")



ingestion_pipeline.ingest(file_path1, "public")
ingestion_pipeline.ingest(file_path2,"employee")
ingestion_pipeline.ingest(file_path3, "admin")
ingestion_pipeline.ingest(file_path4, "admin")
ingestion_pipeline.ingest(file_path5, "public")






