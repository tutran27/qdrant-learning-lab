from qdrant_client import QdrantClient, models
from common.config import settings
from common.embedding import embed_dense, load_dense_model

from labs.lab_07_multitenancy_permission.constant import (
    COLLECTION_NAME,
)

def search_by_tenant(dense_model, query: str, tenant_id: str = "qdrant_labs", limit: int = 5):
    query_vector = embed_dense(dense_model, query)
    client = QdrantClient(path=settings.qdrant_path)
    flt=models.Filter(
        must=[
            models.FieldCondition(
                key="tenant_id",
                match=models.MatchValue(value=tenant_id)
            ),
            models.FieldCondition(
                key="is_deleted",
                match=models.MatchValue(value=False)
            )
        ]
    )
    
    res=client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        query_filter=flt,
        limit=limit,
        with_payload=True,
        with_vectors=False,
    )
    client.close()
    return res.points
    
if __name__ == "__main__":
    import json
    
    dense_model = load_dense_model()
    
    tenant_id = "qdrant_labs"
    query="NoteboolLM dùng làm gì"
    
    results = search_by_tenant(dense_model, query, tenant_id, 2)
    for result in results:
        print(f"ID: {result.id}")
        print(f"Score: {result.score}")
        print(f"Payload: {json.dumps(result.payload, indent=2, ensure_ascii=False)}")
        print("---")