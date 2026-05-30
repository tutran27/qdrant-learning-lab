import json

from qdrant_client import QdrantClient

from common.config import settings
from common.embedding import load_dense_model, load_sparse_model
from labs.lab_09_eval_retrieval.recall_at_k import (
    DEFAULT_EVAL_SET_PATH,
    build_relevant_targets,
    point_to_target,
    retrieve_points,
)


def mrr_at_k_from_points(retrieved_points, relevant_targets: set[tuple[str, int]], k: int) -> float:
    if not relevant_targets:
        return 0.0

    for rank, point in enumerate(retrieved_points[:k], start=1):
        target = point_to_target(point)
        if target in relevant_targets:
            return 1.0 / rank

    return 0.0


def evaluate_mrr_at_k(client, embed_model, query_data: dict, top_k: int = 5) -> float:
    relevant_targets = build_relevant_targets(query_data)
    retrieved_points = retrieve_points(client, embed_model, query_data["query"], top_k)
    mrr = mrr_at_k_from_points(retrieved_points, relevant_targets, top_k)

    retrieved_targets = [
        point_to_target(point)
        for point in retrieved_points[:top_k]
    ]
    print(f"Query: {query_data['id']} | {query_data['query']}")
    print(f"Relevant targets: {sorted(relevant_targets)}")
    print(f"Retrieved targets: {retrieved_targets}")
    print(f"MRR@{top_k}: {mrr}")

    return mrr


def evaluate_mrr(
    client,
    embed_model,
    path: str = DEFAULT_EVAL_SET_PATH,
    top_k: int = 5,
) -> float:
    with open(path, "r", encoding="utf-8") as f:
        eval_set = json.load(f)

    queries = eval_set["queries"]
    total_mrr = 0.0

    for query_data in queries:
        print("=" * 60)
        total_mrr += evaluate_mrr_at_k(client, embed_model, query_data, top_k)

    return total_mrr / len(queries) if queries else 0.0


if __name__ == "__main__":
    client = QdrantClient(path=settings.qdrant_path)
    try:
        print(f"Loading dense model: {settings.embedding_model}")
        dense_model = load_dense_model()
        sparse_model = load_sparse_model()

        mrr = evaluate_mrr(client, [dense_model, sparse_model], top_k=5)
        print(f"Mean MRR@5: {mrr}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()
