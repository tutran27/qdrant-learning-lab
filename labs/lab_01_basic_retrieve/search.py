import json 

from qdrant_client import QdrantClient, models

from common.config import settings
from common.embedding import embedding

def query(client, text: str, limit=3):
    query_vector=embedding(text)
    res=client.query_points(
        collection_name=settings.dense_collection_name,
        query=query_vector,
        limit=limit,
        with_payload=True,
        with_vectors=False
    )
    client.close()
    return res

if __name__ == "__main__":
    client=QdrantClient(path=settings.qdrant_path)

    result, nextpage=client.scroll(
        collection_name=settings.dense_collection_name,
        limit=4,
        with_payload=True,
        with_vectors=False
    )
    print("======== SCROLL ========")
    for res in result:
        print(f"ID: {res.id}")
        print(f"PAYLOAD: {json.dumps(res.payload, indent=2, ensure_ascii=False)}")
        break


    text="NotebookLM có những ưu điểm và nhược điểm gì?"
    res_query=query(client, text)
    print("======== Query ========")
    for x in res_query.points:
        print(f"ID: {x.id}")
        print(f"SCORE: {x.score}")
        print(f"PAYLOAD: {json.dumps(x.payload, indent=2, ensure_ascii=False)}")
        print("---------")

    client.close()
