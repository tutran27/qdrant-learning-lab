from qdrant_client import QdrantClient

from common.config import settings


def ensure_collection_exits(client: QdrantClient):
    if client.collection_exists(collection_name=settings.dense_collection_name):
        client.delete_collection(collection_name=settings.dense_collection_name)
    
   