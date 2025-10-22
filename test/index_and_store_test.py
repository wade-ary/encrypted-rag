import pytest
import sys, os
sys.path.append(os.path.abspath(os.getcwd()))
from data_setup.document_loader.pdf_loader import PDFLoader
from data_setup.document_loader.docx_loader import DocxLoader
from data_setup.document_loader.txt_loader import TxtLoader
from data_setup.embedding_generator.basic_embedder import BasicEmbedder
from data_setup.text_preprocessor.basic_preprocessor import BasicPreprocessor
from data_setup.storage_manager.local_storage_manager import LocalStorageManager
import os
import sys, os
SAMPLE_DIR = "/Users/aryamanwade/Desktop/encrypt_rag/encrypted-rag/test/sample_text"


loader = PDFLoader()
file_path = os.path.join(SAMPLE_DIR, "testing_doc.pdf")
text = loader.load(file_path)
metadata = loader.get_metadata(file_path)

preprocess = BasicPreprocessor()
chunks = preprocess.chunk(text)

embedder = BasicEmbedder()
embeddings = embedder.encode(chunks)

data_store = LocalStorageManager()
data_store.store("sample_doc", chunks, embeddings, metadata)


import json

meta_path = "vector_store/metadata.json"

if os.path.exists(meta_path):
    with open(meta_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if "sample_doc" in data:
        doc = data["sample_doc"]
        print(f"\nDocument ID: sample_doc")
        print(f"Number of chunks: {len(doc['chunks'])}")
        print(f"FAISS IDs: {doc['faiss_ids'][:5]}{'...' if len(doc['faiss_ids']) > 5 else ''}")
        print(f"Metadata: {doc['metadata']}")
    else:
        print("sample_doc not found in metadata.json")
else:
    print("No metadata.json file found.")






