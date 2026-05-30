from qdrant_client import QdrantClient
from common.config import settings
from sentence_transformers import CrossEncoder
import torch

from labs.lab_09_eval_retrieval.retrieve import hybrid_retrieve
from common.embedding import load_dense_model, load_sparse_model

def load_cross_encoder_model():
    return CrossEncoder(settings.cross_encoder_name,
                        activation_fn=torch.nn.Sigmoid())

def rerank(model, query, candidates, top_n=5, threshold:float = 0.5):
    if not candidates:
        return {
            "status": "No candidates",
            "results": []
        }
    pairs = [(query, x.payload.get("text", "")) for x in candidates]
    scores = model.predict(pairs, batch_size=10, show_progress_bar=False)
    
    for item, score in zip(candidates, scores):
        search_score = item.score
        rerank_score=search_score+score
        item.payload["rerank_score"]=score
        item.payload["final_score"]=rerank_score
    
    candidates_sorted = sorted(candidates, key=lambda x: x.payload['final_score'], reverse=True)
    final_rerank_results = [x for x in candidates_sorted[:top_n] ]
    if threshold:
        final_rerank_results = [x for x in final_rerank_results if x.payload['final_score'] > threshold]
        print(f"after rerank filter : {len(final_rerank_results)}")

    if len(final_rerank_results) > top_n:
        final_rerank_results = final_rerank_results[:top_n]
    elif len(final_rerank_results) == 0:
        return {
            "status": "No candidates after rerank filter",
            "results": []
        }
    return {
        "status": "Success",
        "results": final_rerank_results
    }
    
if __name__=="__main__":
    client=QdrantClient(path=settings.qdrant_path)
    
    model=load_cross_encoder_model()
    dense_model=load_dense_model()
    sparse_model=load_sparse_model()
    print("Cross encoder model loaded")
    
    query="Sứ mệnh lịch sử của giai cấp công nhân"
    candidates=hybrid_retrieve(client, dense_model, sparse_model, query, top_k=10)
    print("Hybrid retrieve results:", len(candidates))
    
    result=rerank(model, query, candidates, top_n=5)
    print("Rerank results:", len(result["results"]))
    
    for item in result["results"]:
        print(f"ID: {item.id}, Score: {item.payload['final_score']}, Text: {item.payload['text']}")
        print(f"Rerank Score: {item.payload['rerank_score']}")
        print(f"Search Score: {item.score}")
        print("-" * 50)
    client.close()
    