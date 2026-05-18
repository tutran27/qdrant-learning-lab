import json

from qdrant_client import QdrantClient, models

from common.config import settings
from common.embedding import embed_dense, load_dense_model, embed_sparse, load_sparse_model
from labs.lab_04_hybrid_dense_sparse.constants import (
    COLLECTION_NAME,
    DEFAULT_LIMIT,
    DEFAULT_PREFETCH_LIMIT,
    DENSE_VECTOR_NAME,
    SPARSE_VECTOR_NAME,
)

def hybrid_search(client: QdrantClient, 
                dense_model, 
                sparse_model, 
                query, 
                flt = None,
                k=DEFAULT_PREFETCH_LIMIT,
                top_k=DEFAULT_LIMIT,
                ):
    dense_vectors=embed_dense(dense_model, [query])
    sparse_vectors=embed_sparse(sparse_model, [query])

    result=client.query_points(
        collection_name=COLLECTION_NAME,
        prefetch=[
            models.Prefetch(
                query=dense_vectors[0].tolist(),
                limit=k,
                filter=flt,
                using=DENSE_VECTOR_NAME
            ),
            models.Prefetch(
                query=sparse_vectors[0],
                limit=k,
                filter=flt,
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
    return result.points


if __name__ == "__main__":
    client=QdrantClient(path=settings.qdrant_path)
    dense_model=load_dense_model()
    sparse_model=load_sparse_model()
    query="notebooklm có thể làm gì?"
    flt=models.Filter(
        must=[
            models.FieldCondition(
                key="file_name",
                match=models.MatchValue(
                    value="[Description]-Building-Simple-NotebookLM.pdf"
                )
            ),
            models.FieldCondition(
                key="is_deleted",
                match=models.MatchValue(value=False)
            )
        ]
    )
    
    results=hybrid_search(client, dense_model, sparse_model, query, flt)
    print("======== Hybrid Search ========")
    for res in results:
        print(f"ID: {res.id}")
        print(f"PAYLOAD: {json.dumps(res.payload, indent=2, ensure_ascii=False)}")
        print(f"Score: {res.score}")
        print("----------")
    client.close()
    
    
    
    
    
