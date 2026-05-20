from qdrant_client import QdrantClient, models

from common.config import settings

COLLECTION_NAME= COLLECTION_NAME = f"{settings.dense_collection_name}_lab01"
def ensure_collection_exists(client: QdrantClient):
    if client.collection_exists(collection_name=COLLECTION_NAME):
        client.delete_collection(collection_name=COLLECTION_NAME)
        print(f"Deleted collection {COLLECTION_NAME}")
    
    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=models.VectorParams(
            size=settings.vector_size,
            distance=models.Distance.COSINE
        )
    )

    print(f"Created collection {COLLECTION_NAME}")


ensure_collection_exits = ensure_collection_exists

if __name__ == "__main__":
    client = QdrantClient(path=settings.qdrant_path)
    try:
        ensure_collection_exists(client)
    finally:
        client.close()

    
   
