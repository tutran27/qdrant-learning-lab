import json

from qdrant_client import QdrantClient
from common.embedding import embed_dense, load_dense_model
from common.config import settings
from labs.lab_04_hybrid_dense_sparse.constants import COLLECTION_NAME, DENSE_VECTOR_NAME
from labs.lab_09_eval_retrieval.retrieve import dense_retrieve

def evaluate_recall_at_k(client, dense_model,query, relevant_pages, top_n: int = 5):  
    if not relevant_pages:
        return 0.0
    retrieved_points = dense_retrieve(client, dense_model,query, top_n)
    retrieve_set=set([x.payload["metadata"]["page"] for x in retrieved_points])
    relevant_set=set(relevant_pages)
    print(f"retrieve_set: {retrieve_set}")
    print(f"relevant_set: {relevant_set}")
    hit_count=sum(1 for x in retrieve_set if x in relevant_set)
    print(f"hit_count: {hit_count}")
    return hit_count/len(relevant_pages)

def evaluate_recall(client , dense_model, path = "labs/lab_09_eval_retrieval/eval_set.json",top_n: int = 5):
    with open(path, "r", encoding="utf-8") as f:
        eval_set = json.load(f)
    
    total_recall = 0
    num_queries = len(eval_set["queries"])
    for query_data in eval_set["queries"]:
        print(f"===========================================================")
        recall = evaluate_recall_at_k(client, dense_model, query_data["query"], query_data["relevant_pages"], top_n)
        
        print(f"Query: {query_data['query']} | Relevant pages: {query_data['relevant_pages']} | Recall@k: {recall}")
        total_recall += recall
    return total_recall / num_queries

if __name__ == "__main__":
    client = QdrantClient(path=settings.qdrant_path)
    try:
        print(f"Loading dense model: {settings.embedding_model}")
        dense_model = load_dense_model()
        query="Qdrant là gì và nó giải quyết bài toán nào trong hệ thống AI?"
        relevant_pages=[4]
        
        # recall_at_k=evaluate_recall_at_k(client, dense_model, query, relevant_pages)
        # print(f"Recall@k: {recall_at_k}")

        print(f"================== Evaluate Recall=======================\n")
        recall=evaluate_recall(client, dense_model)
        print(f"Recall: {recall}")
    finally:
        client.close()