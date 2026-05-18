import json

from qdrant_client import QdrantClient
from common.config import settings

from common.embedding import load_dense_model, embed_dense
from labs.lab_04_hybrid_dense_sparse.constants import (
    COLLECTION_NAME,
    DEFAULT_LIMIT,
    DENSE_VECTOR_NAME,
)

def dense_search(client, dense_model, collection_name, query, limit=DEFAULT_LIMIT):
   query_vector=embed_dense(dense_model, [query])
   result=client.query_points(
       collection_name=collection_name,
       query=query_vector[0].tolist(),
       limit=limit,
       using=DENSE_VECTOR_NAME,
       with_payload=True,
       with_vectors=True
   )
   
   return result
   
if __name__ == "__main__":
    client=QdrantClient(path=settings.qdrant_path)
    dense_model=load_dense_model()
    query="notebooklm có thể làm gì?"
    results=dense_search(client, dense_model, COLLECTION_NAME, query)
    print("======== Dense Search ========")
    for res in results.points:
        print(f"ID: {res.id}")
        print(f"PAYLOAD: {json.dumps(res.payload, indent=2, ensure_ascii=False)}")
        print(f"Score: {res.score}")
        print("----------")
    client.close()
