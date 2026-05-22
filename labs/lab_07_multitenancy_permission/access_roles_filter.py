from qdrant_client import QdrantClient, models
from common.config import settings
from common.embedding import load_dense_model, embed_dense 

from labs.lab_07_multitenancy_permission.constant import (
    COLLECTION_NAME
)

def build_access_filter(tenant_id: str, user_roles: list[str]):
    print("Tạo filter với tenant_id:", tenant_id, "và user_roles:", user_roles)
    return models.Filter(
        must=[
            models.FieldCondition(
                key="tenant_id",
                match=models.MatchValue(
                    value=tenant_id
                )
            ),
            models.FieldCondition(
                key="is_deleted",
                match=models.MatchValue(
                    value=False
                )
            ),
            models.Filter(
                should=[
                    models.FieldCondition(
                        key="access_roles",
                        match=models.MatchAny(
                            any=user_roles
                        )
                    ),
                    models.FieldCondition(
                        key="visibility",
                        match=models.MatchValue(
                            value="public"
                        )
                    )
                ]
            )
            
        ]
    )
     
def search(query: str, dense_model, tenant_id: str = "qdrant_labs", user_roles: list[str] = ["viewer"], limit: int = 5):
    query_vector = embed_dense(dense_model, query)
    
    client = QdrantClient(path=settings.qdrant_path)
    filter = build_access_filter(tenant_id, user_roles)
    print("Đang tìm kiếm...")
    res_search = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        query_filter=filter,
        limit=limit,
        with_payload=True,
        with_vectors=False
    )
    return res_search.points

if __name__ == "__main__":
    # Example usage
    import json
    query = "Quy trình tạo ra NoteBookLM"
    tenant_id = "qdrant_labs"
    user_roles = ["viewer"]
    dense_model = load_dense_model()
    results = search(query, dense_model, tenant_id, user_roles)
    
    for result in results:
        print(f"ID: {result.id}")
        print(f"Tenant ID: {result.payload.get('tenant_id')}")
        print(f"Access Roles: {result.payload.get('access_roles')}")
        print(f"Visibility: {result.payload.get('visibility')}")
        print("---")
        