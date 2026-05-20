import json
from qdrant_client import QdrantClient

from common.config import settings
from common.embedding import load_colbert_model
from common.embedding import embed_colbert


def search_colbert(client: QdrantClient, query: str, k: int = 5):
    query_colbert=embed_colbert(load_colbert_model(),[query])
    query_colbert=list(query_colbert)[0].tolist()
    result=client.query_points(
        collection_name=settings.colbert_collection_name,
        query=query_colbert,
        limit=k,
        with_payload=True,
        with_vectors=False,
        using="colbert"
    )
    return result.points


if __name__=="__main__":
    client=QdrantClient(path=settings.qdrant_path)
    
    query="Quá trình của mô hình RAG"
    results=search_colbert(client, query, k=5)

    for r in results:
        print(f"ID: {r.id}")
        print(f"Score: {r.score}")
        print(f"Payload: {json.dumps(r.payload, indent=2, ensure_ascii=False)}")
        print("\n")
    client.close()