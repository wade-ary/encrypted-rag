import os
import sys
import json
import pytest

# Add project root to sys.path
sys.path.append(os.path.abspath(os.getcwd()))

from agentic_function.mistral_agent import MistralAgent
from conversation_memory.memory_manager import ConversationMemory
from data_setup.document_ingestion_pipeline.basic_ingestion_pipeline import BasicIngestionPipeline
from data_setup.document_loader.pdf_loader import PDFLoader
from data_setup.embedding_generator.basic_embedder import BasicEmbedder
from data_setup.text_preprocessor.basic_preprocessor import BasicPreprocessor
from data_setup.storage_manager.local_storage_manager import LocalStorageManager
from retrieval_architecture.MetadataRetrieval.basic_metadata_retrieval import BasicMetadataRetrieval
from retrieval_architecture.VectorIndexRetrieval.basic_vector_retrieval import BasicVectorRetrieval
from retrieval_architecture.RetrieverPipelines.basic_retriever_pipeline import BasicRetrieverPipeline
from data_setup.encryption_system.basic_encryption import  BasicEncryption
from data_setup.encryption_system.aes_encryption import AESEncryption

DATA_STORE = "/Users/aryamanwade/Desktop/encrypt_rag/encrypted-rag/data_store"
metadata_retrieval = BasicMetadataRetrieval(
    metadata_path=os.path.join(DATA_STORE, "aes_embedding_map.json")
)
vector_retrieval = BasicVectorRetrieval(
    index_path=os.path.join(DATA_STORE, "aes_test_faiss_index.bin")
)
encryption = AESEncryption()
retrieval_pipeline = BasicRetrieverPipeline(vector_retrieval, metadata_retrieval, encryption)
def chat_loop():
    memory = ConversationMemory()
    agent = MistralAgent()
    while True:
        user_query = input("\nUser: ").strip()
        if user_query.lower() in ["exit", "quit"]:
            print("Chat ended.")
            break
        permission = input("Permission level: ").strip()
        num_result = input("Number of results: ").strip()
        # Load recent context
        recent_turns = memory.get_last_turns(n=3)

        # Optionally format it for the model
        context = "\n".join(
            [f"User: {t['user_query']}\nAssistant: {t['response']}" for t in recent_turns]
        )

        # Pass context into refinement + summarization
        refined = agent.refine_query(user_query, context=context)
        chunks = retrieval_pipeline.retrieve(refined, int(num_result),permission)
        response = agent.summarize(chunks, context=context)

        print(f"\nAssistant: {response}")

        memory.add_turn(
            user_query,
            refined,
            response,
            permission)

if __name__ == '__main__':
    chat_loop()

