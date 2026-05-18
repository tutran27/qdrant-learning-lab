from qdrant_client import QdrantClient

from common.config import settings
from common.embedding import load_dense_model, load_sparse_model

from labs.lab_04_hybrid_dense_sparse.constants import COLLECTION_NAME, DEFAULT_LIMIT
from labs.lab_04_hybrid_dense_sparse.dense_search import dense_search
from labs.lab_04_hybrid_dense_sparse.hybrid_rrf import hybrid_search
from labs.lab_04_hybrid_dense_sparse.sparse_search import sparse_search


QUERIES = [
    "NotebookLM có thể làm gì?",
    "vector database dùng để làm gì?",
    "agent memory nên lưu thông tin gì?",
]


def text_preview(text: str, max_len: int = 180) -> str:
    text = " ".join(text.split())
    if len(text) <= max_len:
        return text
    return text[:max_len] + "..."


def print_results(name: str, points):
    print(f"\n======== {name} ========")
    for rank, point in enumerate(points, start=1):
        payload = point.payload or {}
        print(f"Rank: {rank}")
        print(f"Score: {point.score}")
        print(f"File: {payload.get('file_name')}")
        print(f"Page: {payload.get('page')}")
        print(f"Text: {text_preview(payload.get('text', ''))}")
        print("----------")


def print_overlap(dense_points, sparse_points, hybrid_points):
    dense_ids = {point.id for point in dense_points}
    sparse_ids = {point.id for point in sparse_points}
    hybrid_ids = {point.id for point in hybrid_points}

    print("\n======== Overlap Top-k ========")
    print(f"Dense ∩ Sparse: {len(dense_ids & sparse_ids)}")
    print(f"Dense ∩ Hybrid: {len(dense_ids & hybrid_ids)}")
    print(f"Sparse ∩ Hybrid: {len(sparse_ids & hybrid_ids)}")


def method_summary(points):
    if not points:
        return "Không có kết quả"

    payload = points[0].payload or {}
    return f"{payload.get('file_name')} | page {payload.get('page')} | score {points[0].score:.4f}"


def compare_query(client, dense_model, sparse_model, query):
    dense_result = dense_search(
        client=client,
        dense_model=dense_model,
        collection_name=COLLECTION_NAME,
        query=query,
        limit=DEFAULT_LIMIT,
    )
    sparse_result = sparse_search(
        client=client,
        model=sparse_model,
        collection_name=COLLECTION_NAME,
        query=query,
        limit=DEFAULT_LIMIT,
    )
    hybrid_points = hybrid_search(
        client=client,
        dense_model=dense_model,
        sparse_model=sparse_model,
        query=query,
        top_k=DEFAULT_LIMIT,
    )

    dense_points = dense_result.points
    sparse_points = sparse_result.points

    print(f"\n\nQuery: {query}")
    print_results("Dense Search", dense_points)
    print_results("Sparse Search", sparse_points)
    print_results("Hybrid RRF", hybrid_points)
    print_overlap(dense_points, sparse_points, hybrid_points)

    print("\n======== Summary ========")
    print(f"Dense top 1 : {method_summary(dense_points)}")
    print(f"Sparse top 1: {method_summary(sparse_points)}")
    print(f"Hybrid top 1: {method_summary(hybrid_points)}")


if __name__ == "__main__":
    client = QdrantClient(path=settings.qdrant_path)
    dense_model = load_dense_model()
    sparse_model = load_sparse_model()

    try:
        for query in QUERIES:
            compare_query(client, dense_model, sparse_model, query)
    finally:
        client.close()
