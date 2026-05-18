import json

from qdrant_client import QdrantClient, models
from common.config import settings

from common.embedding import load_dense_model, embed_dense

def dense_search(client, dense_model, collection_name, query):
   query_vector=embed_dense(dense_model, [query])
   result=client.query_points(
       collection_name=collection_name,
       query=query_vector[0].tolist(),
       limit=4,
       using='dense',
       with_payload=True,
       with_vectors=True
   )
   
   return result
   
if __name__ == "__main__":
    client=QdrantClient(path=settings.qdrant_path)
    collection_name=settings.dense_collection_name + "_lab04"
    dense_model=load_dense_model()
    query="notebooklm có thể làm gì?"
    results=dense_search(client, dense_model, collection_name, query)
    print("======== Dense Search ========")
    for res in results.points:
        print(f"ID: {res.id}")
        print(f"PAYLOAD: {json.dumps(res.payload, indent=2, ensure_ascii=False)}")
        print(f"Score: {res.score}")
        print("----------")
    client.close()