from qdrant_client import QdrantClient, models
from common.config import settings

COLLECTION_NAME = f"{settings.dense_collection_name}_law_tenant"

def ensure_collection(client: QdrantClient):
    client.recreate_collection(
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

    TENANT_INDEX = [
        ("tenant_id", 
            models.KeywordIndexParams(type=models.KeywordIndexType.KEYWORD, is_tenant=True)
        )
    ]
    
    PAYLOAD_INDEX = [
        ("user_id", models.KeywordIndexParams(type=models.KeywordIndexType.KEYWORD)),
        ("access_roles", models.KeywordIndexParams(type=models.KeywordIndexType.KEYWORD)),
        ("visibility", models.KeywordIndexParams(type=models.KeywordIndexType.KEYWORD)),
        
        ("file_name", models.KeywordIndexParams(type=models.KeywordIndexType.KEYWORD)),
        ("source", models.KeywordIndexParams(type=models.KeywordIndexType.KEYWORD)),
        ("doc_type", models.KeywordIndexParams(type=models.KeywordIndexType.KEYWORD)),
        ("lang", models.KeywordIndexParams(type=models.KeywordIndexType.KEYWORD)),

        ("title", models.TextIndexParams(type=models.TextIndexType.TEXT)),
        ("is_deleted", models.BoolIndexParams(type=models.BoolIndexType.BOOL)),
    ]

    create_payload_index(client, PAYLOAD_INDEX)
    create_tenant_index(client, TENANT_INDEX)
    client.close()
