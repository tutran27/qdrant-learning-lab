import json
from qdrant_client import QdrantClient, models

from common.config import settings
from labs.lab_04_hybrid_dense_sparse.constants import (
    COLLECTION_NAME,
    DEFAULT_LIMIT,
    DENSE_VECTOR_NAME,
    SPARSE_VECTOR_NAME,
)

def scroll_collection(client, collection_name, flt=None, limit=DEFAULT_LIMIT):
    result, nextpage=client.scroll(
        collection_name=collection_name,
        limit=limit,
        scroll_filter=flt,
        with_payload=True,
        with_vectors=True
    )
    print("======== SCROLL ========")
    for res in result:
        print(f"ID: {res.id}")
        print(f"PAYLOAD: {json.dumps(res.payload, indent=2, ensure_ascii=False)}")
        # print(f"Vector: {res.vector[DENSE_VECTOR_NAME]}")
        # print(f"Sparse: {res.vector[SPARSE_VECTOR_NAME]}")
        print("----------")


if __name__ == "__main__":
    client=QdrantClient(path=settings.qdrant_path)
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
    scroll_collection(client, COLLECTION_NAME, flt)
    client.close()
