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


# --- Paths ---
SAMPLE_DIR = "/Users/aryamanwade/Desktop/encrypt_rag/encrypted-rag/test/sample_text"
DATA_STORE = "/Users/aryamanwade/Desktop/encrypt_rag/encrypted-rag/data_store"
OUTPUT_FILE = os.path.join(DATA_STORE, "retrieval_test_results.txt")


# --- Component Setup ---
pdf_loader = PDFLoader()
embedding_generator = BasicEmbedder()
preprocessor = BasicPreprocessor(chunk_size=200, overlap=20)
storage_manager = LocalStorageManager(
    storage_path=os.path.join(DATA_STORE, "embedding_map.json")
)

# --- Ingest PDFs ---
pdf_files = ["un_office_drugs.pdf", "europol.pdf", "global_initiatives.pdf"]

for pdf_name in pdf_files:
    file_path = os.path.join(SAMPLE_DIR, pdf_name)
    text = pdf_loader.load(file_path)
    metadata = pdf_loader.get_metadata(file_path)
    chunks = preprocessor.chunk(text)
    embeddings = embedding_generator.encode(chunks)
    storage_manager.store(pdf_name[:-4], chunks, embeddings, metadata)


# --- Retrieval Setup ---
metadata_retrieval = BasicMetadataRetrieval(
    metadata_path=os.path.join(DATA_STORE, "embedding_map.json")
)
vector_retrieval = BasicVectorRetrieval(
    index_path=os.path.join(DATA_STORE, "faiss_index.bin")
)
retrieval_pipeline = BasicRetrieverPipeline(vector_retrieval, metadata_retrieval)


# --- Run Sample Queries ---
queries = {
    "Main methods of drug trafficking in the EU": None,
    "Country with the highest influence in the european drug trade": None,
    "Most prominent drug trafficked through the EU": None
}

for q_text in queries.keys():
    results = retrieval_pipeline.retrieve(query=q_text, top_k=3)
    queries[q_text] = results


# --- Save Results to File ---
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for query, results in queries.items():
        f.write(f"=== Query: {query} ===\n\n")
        for i, result in enumerate(results, 1):
            f.write(f"Result {i}:\n")
            f.write(f"Document ID: {result.get('doc_id', 'N/A')}\n")
            f.write(f"Score: {result.get('score', 'N/A'):.4f}\n")
            f.write(f"Chunk:\n{result.get('chunk', '')}\n\n")
        f.write("=" * 60 + "\n\n")

print(f"✅ Retrieval test complete. Results saved to:\n{OUTPUT_FILE}")