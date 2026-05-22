from pydantic import dataclasses
from dotenv import load_dotenv
import os
import torch

load_dotenv()

@dataclasses.dataclass
class Settings:
    qdrant_path: str = os.getenv("QDRANT_PATH", "./qdrant_storage")
    dense_collection_name: str = os.getenv("DENSE_COLLECTION_NAME", "documents")
    hybrid_collection_name: str = os.getenv("HYBRID_COLLECTION_NAME", "hybrid_documents")
    colbert_collection_name: str = os.getenv("COLBERT_COLLECTION_NAME", "colbert_documents")
    cross_encoder_name: str = os.getenv(
        "CROSS_ENCODER_NAME",
        "cross-encoder/mmarco-mMiniLMv2-L12-H384-v1",
    )
    vector_size: int = 768
    use_cuda: str = "cuda" if torch.cuda.is_available() else "cpu"

    hf_token: str = os.getenv("HF_TOKEN")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "bkai-foundation-models/vietnamese-bi-encoder")
    sparse_embedding_model = os.getenv("SPARSE_EMBEDDING_MODEL", "Qdrant/bm25")
    colbert_model_name: str = os.getenv("COLBERT_MODEL_NAME", "colbert-ir/colbertv2.0")    
    
    groq_api_key: str = os.getenv("GROQ_API_KEY")
    groq_model: str = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
    
    chunk_size: int = 512
    chunk_overlap: int = 128
    max_retries: int = 3

settings = Settings()

if __name__ == "__main__":
    print("=== Configuration ===")  
    print(f"Qdrant Path: {settings.qdrant_path}")
    print(f"Dense Collection Name: {settings.dense_collection_name}")
    print(f"Hybrid Collection Name: {settings.hybrid_collection_name}")
    print(f"Embedding Model: {settings.embedding_model}")
    print(f"Chunk Size: {settings.chunk_size}")
    print(f"Chunk Overlap: {settings.chunk_overlap}")
    print(f"Max Retries: {settings.max_retries}")
    print(f"HF Token: {settings.hf_token}")
    print("=====================")
