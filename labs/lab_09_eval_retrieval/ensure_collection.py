from qdrant_client import QdrantClient, models

from common.config import settings

COLLECTION_NAME = f"{settings.dense_collection_name}_lab09"

def ensure_colbert_collection(client:QdrantClient, collection_name: str = COLLECTION_NAME, vector_size=128):
    if client.collection_exists(collection_name=collection_name):
        print("ColBERT collection already exists")
        client.delete_collection(collection_name=collection_name)
    
    client.create_collection(
        collection_name=collection_name,
        vectors_config={
            "dense": models.VectorParams(
                size=768,
                distance=models.Distance.COSINE
            ),
            "colbert": models.VectorParams(
                size=vector_size,
                distance=models.Distance.COSINE,
                multivector_config=models.MultiVectorConfig(
                    comparator=models.MultiVectorComparator.MAX_SIM
                )
            )
        },
        sparse_vectors_config = {
            "sparse": models.SparseVectorParams()
        }
    )
    print("ColBERT collection created")
    
if __name__ == "__main__":
    client = QdrantClient(path=settings.qdrant_path)
    try:
        ensure_colbert_collection(client, collection_name=COLLECTION_NAME)
    finally:
        client.close()