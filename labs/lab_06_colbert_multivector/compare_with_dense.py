import json

from qdrant_client import QdrantClient

from common.config import settings
from common.embedding import load_dense_model
from labs.lab_04_hybrid_dense_sparse.constants import COLLECTION_NAME
from labs.lab_04_hybrid_dense_sparse.dense_search import dense_search
from labs.lab_06_colbert_multivector.colbert_search import search_colbert


def preview_text(text: str, max_len: int = 220) -> str:
    text = " ".join((text or "").split())
    if len(text) <= max_len:
        return text
    return text[:max_len] + "..."


def print_results(title: str, points):
    print(f"\n======== {title} ========")

    for rank, point in enumerate(points, start=1):
        payload = point.payload or {}

        print(f"\nRank: {rank}")
        print(f"ID: {point.id}")
        print(f"Score: {point.score:.6f}")
        print(f"File: {payload.get('file_name')}")
        print(f"Page: {payload.get('page')}")
        print(f"Text: {preview_text(payload.get('text'))}")


def compare(query: str, k: int = 5):
    client = QdrantClient(path=settings.qdrant_path)

    try:
        dense_model = load_dense_model()

        dense_result = dense_search(
            client=client,
            dense_model=dense_model,
            collection_name=COLLECTION_NAME,
            query=query,
            limit=k,
        )

        colbert_points = search_colbert(
            client=client,
            query=query,
            k=k,
        )

        print(f"Query: {query}")
        print_results("Dense Search", dense_result.points)
        print_results("ColBERT Multivector Search", colbert_points)

    finally:
        client.close()


if __name__ == "__main__":
    query = "Quá trình của mô hình RAG"
    compare(query=query, k=5)
