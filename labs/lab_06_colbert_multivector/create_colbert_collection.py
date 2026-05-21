from qdrant_client import QdrantClient, models

from common.config import settings

COLLECTION_NAME=settings.colbert_collection_name

def ensure_colbert_collection(client:QdrantClient, vector_size=3072):
    if client.collection_exists(collection_name=COLLECTION_NAME):
        print("ColBERT collection already exists")
        client.delete_collection(collection_name=COLLECTION_NAME)
    else:
        client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config={
            "colbert": models.VectorParams(
                size=vector_size,
                distance=models.Distance.COSINE,
                multivector_config=models.MultiVectorConfig(
                    comparator=models.MultiVectorComparator.MAX_SIM
                )
            )
        }
    )