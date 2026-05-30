from qdrant_client import QdrantClient
from common.config import settings

import json
def scroll(client: QdrantClient, collection_name: str):
    result, next_offset = client.scroll(
        collection_name=collection_name,
        limit=5,
        with_payload=True,
        with_vectors=True,
    )
    for point in result:
        print(f"ID: {point.id}")
        print(f" Length of vector: {len(point.vector)}")
        print(f" Key of vector: {list(point.vector.keys())}")
        print(f"Payload: {json.dumps(point.payload, indent=2, ensure_ascii=False)}")
        break
    return result

if __name__ == "__main__":
    client = QdrantClient(path=settings.qdrant_path)
    collection_name = f"{settings.dense_collection_name}_lab09"

    scroll(client, collection_name)
    client.close()
