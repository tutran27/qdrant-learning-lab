from qdrant_client import QdrantClient, models

from common.config import settings
from labs.lab_04_hybrid_dense_sparse.constants import (
    COLLECTION_NAME,
    DENSE_VECTOR_NAME,
    SPARSE_VECTOR_NAME,
)

def ensure_collection_exists(client):
    collection_name=COLLECTION_NAME
    if client.collection_exists(collection_name=collection_name):
        client.delete_collection(collection_name=collection_name)
        print(f"Deleted collection {collection_name}")
    
    client.create_collection(
        collection_name=collection_name,
        vectors_config={
            DENSE_VECTOR_NAME: models.VectorParams(
                size=settings.vector_size,
                distance=models.Distance.COSINE
            )
        },
        sparse_vectors_config={
            SPARSE_VECTOR_NAME: models.SparseVectorParams()
        }
    )
    print(f"Created collection {collection_name}")

if __name__ == "__main__":
    client=QdrantClient(path=settings.qdrant_path)
    ensure_collection_exists(client)
    
    client.close()
