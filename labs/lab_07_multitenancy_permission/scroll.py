import json
from qdrant_client import QdrantClient
from common.config import settings


COLLECTION_NAME = "documents_law_tenant"
def scroll():
    client = QdrantClient(path=settings.qdrant_path)
    points, next_offset = client.scroll(
        collection_name=COLLECTION_NAME,
        scroll_filter=None,
        limit=2,
        with_payload=True,
        with_vectors=False,
    )
    for point in points:
        print(f"ID: {point.id}")
        print(json.dumps(point.payload, indent=2, ensure_ascii=False))
        break
    client.close()

if __name__ == "__main__":
    scroll()