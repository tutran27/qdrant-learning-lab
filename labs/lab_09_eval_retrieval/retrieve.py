import json

from qdrant_client import QdrantClient, models

from common.config import settings
from common.embedding import embed_dense, load_dense_model, embed_sparse, load_sparse_model, load_colbert_model, embed_colbert
from labs.lab_04_hybrid_dense_sparse.constants import COLLECTION_NAME, DENSE_VECTOR_NAME, SPARSE_VECTOR_NAME


def dense_retrieve(
    client: QdrantClient,
    dense_model,
    query: str,
    top_n: int = 3,
    collection_name: str = COLLECTION_NAME,
):
    query_vector = embed_dense(dense_model, [query])

    search_result = client.query_points(
        collection_name=collection_name,
        query=query_vector[0].tolist(),
        limit=top_n,
        using=DENSE_VECTOR_NAME,
        with_payload=True,
        with_vectors=False,
    )
    return search_result.points

def hybrid_retrieve(
    client: QdrantClient,
    dense_model,
    sparse_model,
    query: str,
    top_k: int = 10,
    top_n: int = 3,
    collection_name: str = COLLECTION_NAME,
):
    dense_vectors = embed_dense(dense_model, [query])
    sparse_vectors = embed_sparse(sparse_model, [query])
    
    result = client.query_points(
        collection_name=collection_name,
        prefetch=[
            models.Prefetch(
                query=dense_vectors[0].tolist(),
                limit=top_k,
                filter=None,
                using=DENSE_VECTOR_NAME
            ),
            models.Prefetch(
                query=sparse_vectors[0],
                limit=top_k,
                filter=None,
                using=SPARSE_VECTOR_NAME
            ),
        ],
        query=models.FusionQuery(
            fusion=models.Fusion.RRF
        ),
        limit=top_n,
        with_payload=True,
        with_vectors=False,
    )
    return result.points
    
if __name__ == "__main__":
    client = QdrantClient(path=settings.qdrant_path)
    try:
        print(f"Loading dense model: {settings.embedding_model}", flush=True)
        dense_model = load_dense_model()
        
        print(f"Loading sparse model: {settings.sparse_embedding_model}", flush=True)
        sparse_model = load_sparse_model()

        print("Retrieving...", flush=True)
        query = "Hạn chế của RAG truyền thống là gì"
        print(f"Query: {query}")
        dense_search_result = dense_retrieve(client, dense_model, query)
        hybrid_search_result = hybrid_retrieve(client, dense_model, sparse_model, query)
        
        print("Hybrid retrieving done", flush=True)

        print("================ Dense Search Result =================")
        for x in dense_search_result:
            print(f"Score: {x.score}")
            print(f"Payload: {json.dumps(x.payload, ensure_ascii=False, indent=2)}")
        
        print("================ Hybrid Search Result =================")
        for x in hybrid_search_result:
            print(f"Hybrid Score: {x.score}")
            print(f"Hybrid Payload: {json.dumps(x.payload, ensure_ascii=False, indent=2)}")
    finally:
        client.close()
