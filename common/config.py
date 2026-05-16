from pydantic import dataclasses
from dotenv import load_dotenv
import os

load_dotenv()

@dataclasses.dataclass
class Settings:
    qdrant_path: str = "./qdrant_storage"
    dense_collection_name: str = "documents"
    hybrid_collection_name: str = "hybrid_documents"
    vector_size: int = 768

    hf_token: str = os.getenv("HF_TOKEN")
    embedding_model: str = "bkai-foundation-models/vietnamese-bi-encoder"
    sparse_embedding_model="Qdrant/bm25"
    chunk_size: int = 512
    chunk_overlap: int = 128
    max_retries: int = 3

settings = Settings()

if __name__ == "__main__":
    print("=== Configuration ===")  
    print(f"Qdrant Path: {settings.qdrant_path}")
    print(f"Collection Name: {settings.collection_name}")
    print(f"Embedding Model: {settings.embedding_model}")
    print(f"Chunk Size: {settings.chunk_size}")
    print(f"Chunk Overlap: {settings.chunk_overlap}")
    print(f"Max Retries: {settings.max_retries}")
    print(f"HF Token: {settings.hf_token}")
    print("=====================")
