import json
from qdrant_client import QdrantClient, models

from common.config import settings
from common.embedding import (
    load_dense_model,
    load_sparse_model,
    embed_dense,
    embed_sparse
    )
from labs.lab_04_hybrid_dense_sparse.constants import (   COLLECTION_NAME,
    DENSE_VECTOR_NAME, 
    SPARSE_VECTOR_NAME, 
    DEFAULT_LIMIT, 
    DEFAULT_PREFETCH_LIMIT
    )

def hybrid_search(
    client: QdrantClient, 
    query: str, 
    dense_model, 
    sparse_model, 
    k: int=DEFAULT_PREFETCH_LIMIT,
    top_k = DEFAULT_LIMIT
):
    dense_vector=embed_dense(dense_model, [query])
    sparse_vector=embed_sparse(sparse_model, [query])[0]

    search_result=client.query_points(
        collection_name=COLLECTION_NAME,
        prefetch=[
            models.Prefetch(
                query=dense_vector[0].tolist(),
                limit=k,
                using=DENSE_VECTOR_NAME
            ),
            models.Prefetch(
                query=sparse_vector,
                limit=k,
                using=SPARSE_VECTOR_NAME
            ),
        ],
        query=models.FusionQuery(
            fusion=models.Fusion.RRF
        ),
        limit=top_k,
        with_payload=True,
        with_vectors=False
    )
    return search_result.points
    
if __name__ == "__main__":
    client=QdrantClient(path=settings.qdrant_path)
    dense_model=load_dense_model()
    sparse_model=load_sparse_model()
    query="What is the best way to train a machine learning model?"
    search_result=hybrid_search(client, query, dense_model, sparse_model,k=DEFAULT_PREFETCH_LIMIT,top_k=DEFAULT_LIMIT)

    print("\n--- Hybrid Search Results ---")
    for hit in search_result:
        print(f"ID: {hit.id}")
        print(f"Score: {hit.score}")
        print(f"Payload: {json.dumps(hit.payload, indent=2, ensure_ascii=False)}")
        print("="*30)
    client.close()