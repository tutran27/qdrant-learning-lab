import json 

from qdrant_client import QdrantClient, models

from common.config import settings
from common.embedding import embedding

if __name__ == "__main__":
    client=QdrantClient(path=settings.qdrant_path)

# ================== UPDATE ====================
# 1. Set_payload
    client.set_payload(
        collection_name=settings.dense_collection_name,
        payload={
            "test_set_payload": "access"
        },
        wait=True
    )

# ================= SCROLL ====================
    result, nextpage=client.scroll(
        collection_name=settings.dense_collection_name,
        limit=4,
        with_payload=True,
        with_vectors=False
    )
    print("======== SCROLL ========")
    for res in result:
        print(f"ID: {res.id}")
        print(f"PAYLOAD: {json.dumps(res.payload, indent=2, ensure_ascii=False)}")
        break
        

# ================== DELETE ====================
    client.close()
