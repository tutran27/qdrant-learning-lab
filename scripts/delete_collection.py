from qdrant_client import QdrantClient
from common.config import settings


def delete_collection(collection_name: str = "hybrid_dense_sparse"):
    client = QdrantClient(path=settings.qdrant_path)
    client.delete_collection(collection_name)
    print(f"Collection {collection_name} deleted successfully")
    client.close()

if __name__ == "__main__":
    COLLECTION_NAME = f"{settings.dense_collection_name}_lab04"
    delete_collection(COLLECTION_NAME)