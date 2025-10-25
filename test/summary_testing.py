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
    metadata_path=os.path.join(DATA_STORE, "embedding_map.json")
)
vector_retrieval = BasicVectorRetrieval(
    index_path=os.path.join(DATA_STORE, "faiss_index.bin")
)
retrieval_pipeline = BasicRetrieverPipeline(vector_retrieval, metadata_retrieval)


# --- Run Sample Queries ---
query =  "Main methods of drug trafficking in the EU"




result = retrieval_pipeline.retrieve(query=query, top_k=5)

basic_summary_gen = BasicSummary() 

test_summary = basic_summary_gen.summarize(result)

# --- Generate and Save Summaries to File ---
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:

    f.write(f"=== Query: {query} ===\n\n")

 

    f.write("Summary:\n")
    f.write(test_summary + "\n\n")
    f.write("=" * 60 + "\n\n")

print(f"✅ Summarization test complete. Summaries saved to:\n{OUTPUT_FILE}")