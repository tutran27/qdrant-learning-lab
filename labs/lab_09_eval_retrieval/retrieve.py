import json

from qdrant_client import QdrantClient

from common.config import settings
from common.embedding import embed_dense, load_dense_model
from labs.lab_04_hybrid_dense_sparse.constants import COLLECTION_NAME, DENSE_VECTOR_NAME


def retrieve(
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


if __name__ == "__main__":
    client = QdrantClient(path=settings.qdrant_path)
    try:
        print(f"Loading dense model: {settings.embedding_model}", flush=True)
        dense_model = load_dense_model()
        print("Dense model loaded", flush=True)

        print("Retrieving...", flush=True)
        search_result = retrieve(client, dense_model, "NotebookLM là gì")
        print("Retrieving done", flush=True)

        for x in search_result:
            print(f"Score: {x.score}")
            print(f"Payload: {json.dumps(x.payload, ensure_ascii=False, indent=2)}")
            break
    finally:
        client.close()
