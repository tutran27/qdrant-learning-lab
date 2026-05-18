import json 

from qdrant_client import QdrantClient, models

from common.config import settings
from common.embedding import embedding

if __name__ == "__main__":
    client=QdrantClient(path=settings.qdrant_path)
    collection_name=settings.dense_collection_name + "_lab02"

# ================== UPDATE ====================
# 1. Set_payload
    client.set_payload(
        collection_name=collection_name,
        payload={
            "test_set_payload": "access",
            "is_delete": False
        },
        points=models.Filter(),
        wait=True
    )

# ================= SCROLL ====================
    result, nextpage=client.scroll(
        collection_name=collection_name,
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
    print("\n======== DELETE ========")
    print("Deleting points...")
    client.delete(
        collection_name=collection_name,
        points_selector=models.FilterSelector(
            filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="page",
                        match=models.MatchValue(value="12/23")
                    )
                ]
            )
        ),
        wait=True
    )
    
   

# ================= SCROLL ====================
    result, nextpage=client.scroll(
        collection_name=collection_name,
        limit=4,
        scroll_filter=models.Filter(
            must=[
                models.FieldCondition(
                    key="page",
                    match=models.MatchValue(value="12/23")
                )
            ]
        ),
        with_payload=True,
        with_vectors=False
    )
    print("======== SCROLL ========")
    for res in result:
        print(f"ID: {res.id}")
        print(f"PAYLOAD: {json.dumps(res.payload, indent=2, ensure_ascii=False)}")
        break 
    
client.close()