from qdrant_client import QdrantClient, models
from common.config import settings
from common.embedding import load_dense_model, embed_dense 

COLLECTION_NAME = f"{settings.dense_collection_name}_law_tenant"

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
     
def search(query, tenant_id: str, user_roles: list[str], limit: int = 5):
    dense_model = load_dense_model()
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
    query = "Quy trình tạo ra NoteBookLM"
    tenant_id = "qdrant_labs"
    user_roles = ["viewer"]
    results = search(query, tenant_id, user_roles)
    
    for result in results:
        print(f"ID: {result.id}")
        print(f"Tenant ID: {result.payload.get('tenant_id')}")
        print(f"Access Roles: {result.payload.get('access_roles')}")
        print(f"Visibility: {result.payload.get('visibility')}")
        print("---")
        