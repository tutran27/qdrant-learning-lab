import json
import statistics
import time

from qdrant_client import QdrantClient

from common.config import settings
from common.embedding import load_dense_model, load_sparse_model
from labs.lab_09_eval_retrieval.retrieve import hybrid_retrieve
from labs.lab_09_eval_retrieval.cross_encoder_rerank import load_cross_encoder_model, rerank

EVAL_SET_PATH = "labs/lab_09_eval_retrieval/eval_set.json"
COLLECTION_NAME = f"{settings.dense_collection_name}_lab09"
TOP_K = 20
TOP_N = 10

def load_queries():
    with open(EVAL_SET_PATH, "r", encoding="utf-8") as f:
        return json.load(f)["queries"]

def timed_hybrid_retrieve(client, dense_model, sparse_model, cross_encoder_model, query: str):
    start = time.perf_counter()
    retrieval_result = hybrid_retrieve(
        client,
        dense_model,
        sparse_model,
        query,
        collection_name=COLLECTION_NAME,
        top_k=TOP_K,
        top_n=TOP_N,
    )
    points= rerank(cross_encoder_model, query, retrieval_result)
    points= points["results"]
    latency_ms = (time.perf_counter() - start) * 1000
    return latency_ms, points

def print_summary(latencies: list[float]):
    latencies = sorted(latencies)
    p95_index = max(0, int(len(latencies) * 0.95) - 1)

    print("\n=== Latency Summary ===")
    print(f"count: {len(latencies)}")
    print(f"mean:  {statistics.mean(latencies):.2f} ms")
    print(f"p50:   {statistics.median(latencies):.2f} ms")
    print(f"p95:   {latencies[p95_index]:.2f} ms")
    print(f"min:   {latencies[0]:.2f} ms")
    print(f"max:   {latencies[-1]:.2f} ms")

if __name__ == "__main__":
    client = QdrantClient(path=settings.qdrant_path)
    try:
        queries = load_queries()
        dense_model = load_dense_model()
        sparse_model = load_sparse_model()
        cross_encoder_model = load_cross_encoder_model()

        print("Warm up...")
        timed_hybrid_retrieve(client, dense_model, sparse_model, cross_encoder_model, queries[0]["query"])

        print(f"Benchmark hybrid retrieval | top_k={TOP_K}, top_n={TOP_N}")
        latencies = []

        for item in queries:
            latency_ms, points = timed_hybrid_retrieve(
                client,
                dense_model,
                sparse_model,
                cross_encoder_model,
                item["query"],
            )
            latencies.append(latency_ms)
            print(f"{item['id']}: {latency_ms:.2f} ms | results={len(points)}")

        print_summary(latencies)
    finally:
        client.close()
