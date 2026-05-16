import json 

from qdrant_client import QdrantClient, models

from common.config import settings

if __name__ == "__main__":
    client=QdrantClient(path=settings.qdrant_path)

    result, nextpage=client.scroll(
        collection_name=settings.dense_collection_name,
        limit=4,
        with_payload=True,
        with_vectors=False
    )

    for res in result:
        print(f"ID: {res.id}")
        print(f"PAYLOAD: {json.dumps(res.payload, indent=2, ensure_ascii=False)}")
        break
