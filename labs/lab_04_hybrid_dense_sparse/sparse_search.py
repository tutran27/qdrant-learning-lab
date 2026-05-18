import json

from qdrant_client import QdrantClient, models

from common.config import settings
from common.embedding import embed_sparse, load_sparse_model

def sparse_search(client, model, collection_name, query):
    query_vector=embed_sparse(model, [query])
    result=client.query_points(
        collection_name=collection_name,
        query=query_vector[0],
        limit=4,
        using="sparse",
        with_payload=True,
        with_vectors=False
    )
    return result

if __name__ == "__main__":
    client=QdrantClient(path=settings.qdrant_path)
    collection_name=settings.dense_collection_name + "_lab04"
    sparse_model=load_sparse_model()
    query="notebooklm có thể làm gì?"
    results=sparse_search(client, sparse_model, collection_name, query)
    print("======== Sparse Search ========")
    for res in results.points:
        print(f"ID: {res.id}")
        print(f"PAYLOAD: {json.dumps(res.payload, indent=2, ensure_ascii=False)}")
        print(f"Score: {res.score}")
        print("----------")
    client.close()