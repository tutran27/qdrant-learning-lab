from qdrant_client import QdrantClient, models
from common.config import settings
from common.embedding import embed_dense, load_dense_model
COLLECTION_NAME = "documents_law_tenant"

def search_by_tenant(dense_model, query: str, tenant_id: str, limit: int = 5):
    query_vector = embed_dense(dense_model, query)
    client = QdrantClient(path=settings.qdrant_path)
    flt=models.Filter(
        must=[
            models.FieldCondition(
                key="tenant_id",
                match=models.MatchValue(value="qdrant_labs")
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