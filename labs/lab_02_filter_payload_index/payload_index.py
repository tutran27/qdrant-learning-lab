from qdrant_client import QdrantClient, models

from common.config import settings

def create_index(client):
    collection_name=settings.dense_collection_name + "_lab02"
    for field_name, field_schema in payload_index:
        client.create_payload_index(
            collection_name=collection_name,
            field_name=field_name,
            field_schema=field_schema,
            wait=True
        )


if __name__ == "__main__":
    payload_index=[
        ("source", models.PayloadSchemaType.KEYWORD),
        ("page", models.PayloadSchemaType.KEYWORD),
        ("is_delete", models.PayloadSchemaType.BOOLEAN)
        ]

    client=QdrantClient(path=settings.qdrant_path)
    create_index(client, payload_index) 
    client.close()