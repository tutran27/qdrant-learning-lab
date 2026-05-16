from qdrant_client import QdrantClient, models

from common.config import settings


def ensure_collection_exists(client: QdrantClient):
    if client.collection_exists(collection_name=settings.dense_collection_name):
        client.delete_collection(collection_name=settings.dense_collection_name)
    
    client.recreate_collection(
        collection_name=settings.dense_collection_name,
        vectors_config=models.VectorParams(
            size=settings.vector_size,
            distance=models.Distance.COSINE
        )
    )

    print(f"Created collection {settings.dense_collection_name}")


ensure_collection_exits = ensure_collection_exists

if __name__ == "__main__":
    client = QdrantClient(path=settings.qdrant_path)
    try:
        ensure_collection_exists(client)
    finally:
        client.close()

    
   
