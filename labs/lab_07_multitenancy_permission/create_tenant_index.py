from qdrant_client import QdrantClient, models
from common.config import settings

from labs.lab_07_multitenancy_permission.constant import (
    COLLECTION_NAME,
    TENANT_INDEX,
    PAYLOAD_INDEX
)

def ensure_collection(client: QdrantClient):
    if client.collection_exists(collection_name=COLLECTION_NAME):
        client.delete_collection(collection_name=COLLECTION_NAME)
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=models.VectorParams(
            size=settings.vector_size,
            distance=models.Distance.COSINE
        )
    )
    print(f"Created collection {COLLECTION_NAME}")

def create_tenant_index(client: QdrantClient, pairs: list[tuple]):
    for field_name, field_schema in pairs:
        client.create_payload_index(
            collection_name=COLLECTION_NAME,
            field_name=field_name,
            field_schema=field_schema
        )
        # field_schema=models.KeywordIndexParams(
        #     type=models.KeywordIndexType.KEYWORD,
        #     is_tenant=True
        # )
        print(f"Created tenant index for {field_name}")

def create_payload_index(client, pairs: list[tuple]):
    for field_name, field_schema in pairs:
        client.create_payload_index(
            collection_name=COLLECTION_NAME,
            field_name=field_name,
            field_schema=field_schema
        )
        print(f"Created payload index for {field_name}")

if __name__=="__main__":
    client=QdrantClient(path=settings.qdrant_path)
    ensure_collection(client)

    create_payload_index(client, PAYLOAD_INDEX)
    create_tenant_index(client, TENANT_INDEX)
    client.close()
