import json

from qdrant_client import QdrantClient

from common.config import settings
from common.embedding import load_dense_model, load_sparse_model
from labs.lab_09_eval_retrieval.retrieve import dense_retrieve, hybrid_retrieve


COLLECTION_NAME = f"{settings.dense_collection_name}_lab09"
DEFAULT_EVAL_SET_PATH = "labs/lab_09_eval_retrieval/eval_set.json"


def build_relevant_targets(query_data: dict) -> set[tuple[str, int]]:
    targets = set()
    for target in query_data.get("relevant_targets", []):
        file_name = target["file_name"]
        for page in target.get("pages", []):
            targets.add((file_name, int(page)))
    return targets


def point_to_target(point) -> tuple[str, int] | None:
    payload = point.payload or {}
    file_name = payload.get("file_name")
    metadata = payload.get("metadata") or {}

    page = metadata.get("page_label")
    if page is None:
        page = int(metadata.get("page")) + 1
    if file_name is None or page is None:
        return None

    return file_name, int(page)

def recall_at_k_from_points(retrieved_points, relevant_targets: set[tuple[str, int]], k: int) -> float:
    if not relevant_targets:
        return 0.0

    retrieved_targets = {
        target
        for point in retrieved_points[:k]
        if (target := point_to_target(point)) is not None
    }
    hits = retrieved_targets & relevant_targets
    return len(hits) / len(relevant_targets)


def retrieve_points(client, embed_model, query: str, top_k: int):
    if len(embed_model) == 1:
        return dense_retrieve(
            client,
            embed_model[0],
            query,
            top_n=top_k,
            collection_name=COLLECTION_NAME,
        )

    return hybrid_retrieve(
        client,
        embed_model[0],
        embed_model[1],
        query,
        collection_name=COLLECTION_NAME,
        top_k=top_k * 2,
        top_n=top_k,
    )


def evaluate_recall_at_k(client, embed_model, query_data: dict, top_k: int = 5) -> float:
    relevant_targets = build_relevant_targets(query_data)
    retrieved_points = retrieve_points(client, embed_model, query_data["query"], top_k)
    recall = recall_at_k_from_points(retrieved_points, relevant_targets, top_k)

    retrieved_targets = [
        point_to_target(point)
        for point in retrieved_points[:top_k]
    ]
    print(f"Query: {query_data['id']} | {query_data['query']}")
    print(f"Relevant targets: {sorted(relevant_targets)}")
    print(f"Retrieved targets: {retrieved_targets}")
    print(f"Recall@{top_k}: {recall}")

    return recall


def evaluate_recall(
    client,
    embed_model,
    path: str = DEFAULT_EVAL_SET_PATH,
    top_k: int = 5,
) -> float:
    with open(path, "r", encoding="utf-8") as f:
        eval_set = json.load(f)

    queries = eval_set["queries"]
    total_recall = 0.0

    for query_data in queries:
        print("=" * 60)
        total_recall += evaluate_recall_at_k(client, embed_model, query_data, top_k)

    return total_recall / len(queries) if queries else 0.0


if __name__ == "__main__":
    client = QdrantClient(path=settings.qdrant_path)
    try:
        print(f"Loading dense model: {settings.embedding_model}")
        dense_model = load_dense_model()
        sparse_model = load_sparse_model()

        recall = evaluate_recall(client, [dense_model, sparse_model], top_k=5)
        print(f"Mean Recall@5: {recall}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()
