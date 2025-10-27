import os
import sys
import json
import pytest

# Add project root to sys.path
sys.path.append(os.path.abspath(os.getcwd()))

# --- Imports ---
from data_setup.document_ingestion_pipeline.basic_ingestion_pipeline import BasicIngestionPipeline
from data_setup.document_loader.pdf_loader import PDFLoader
from data_setup.embedding_generator.basic_embedder import BasicEmbedder
from data_setup.text_preprocessor.basic_preprocessor import BasicPreprocessor
from data_setup.storage_manager.local_storage_manager import LocalStorageManager
from retrieval_architecture.MetadataRetrieval.basic_metadata_retrieval import BasicMetadataRetrieval
from retrieval_architecture.VectorIndexRetrieval.basic_vector_retrieval import BasicVectorRetrieval
from retrieval_architecture.RetrieverPipelines.basic_retriever_pipeline import BasicRetrieverPipeline
from final_summary.basic_summary import BasicSummary

SAMPLE_DIR = "/Users/aryamanwade/Desktop/encrypt_rag/encrypted-rag/test/sample_text"
DATA_STORE = "/Users/aryamanwade/Desktop/encrypt_rag/encrypted-rag/data_store"
OUTPUT_FILE = os.path.join(DATA_STORE, "retrieval_test_summary.txt")


metadata_retrieval = BasicMetadataRetrieval(
    metadata_path=os.path.join(DATA_STORE, "encrypted_embedding_map.json")
)
vector_retrieval = BasicVectorRetrieval(
    index_path=os.path.join(DATA_STORE, "encryption_test_faiss_index.bin")
)
retrieval_pipeline = BasicRetrieverPipeline(vector_retrieval, metadata_retrieval)


# --- Run Sample Queries ---
query =  "Main methods of drug trafficking in the EU"




result_public = retrieval_pipeline.retrieve(query=query, top_k=3, permission="public" )
result_employee = retrieval_pipeline.retrieve(query=query, top_k=3, permission="employee")
result_admin = retrieval_pipeline.retrieve(query=query, top_k=3, permission="admin")

results = {
    "public": result_public,
    "employee": result_employee,
    "admin": result_admin
}

for role, result in results.items():
    output_path = os.path.join(DATA_STORE, f"retrieval_test_{role}.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"=== Query: {query} ===\n\n")
        f.write(f"=== Permission Level: {role.upper()} ===\n\n")
        for i, chunk in enumerate(result, 1):
            f.write(f"Result {i}:\n")
            f.write(f"Document ID: {chunk.get('doc_id', 'N/A')}\n")
            f.write(f"Permission Level: {chunk.get('permission_level', 'N/A')}\n")
            f.write(f"Chunk:\n{chunk.get('chunk', '')}\n\n")
        f.write("=" * 60 + "\n\n")
    print(f"✅ Saved {role} results to: {output_path}")